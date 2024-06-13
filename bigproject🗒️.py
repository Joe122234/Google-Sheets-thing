import gspread
from google.oauth2.service_account import Credentials
import json
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Load the credentials JSON file
with open("credentials.json") as f:
    credentials_info = json.load(f)

# Create the credentials object
creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)

# Authorize the client
client = gspread.authorize(creds)

# Open the Google Sheet by ID
sheet_id = "1OYo5tuzYfkhF5Va55glpou6gsQ10NNWiN2I1ZbGzlHc"
workbook = client.open_by_key(sheet_id)

def add_revenue(product, quantity, price, date=None):
    sheet = workbook.worksheet("Revenue")
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    total_revenue = quantity * price
    sheet.append_row([date, product, quantity, price, total_revenue])
    clear_fields()

def add_expense(expense_type, description, amount, date=None):
    sheet = workbook.worksheet("Expenses")
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([date, expense_type, description, amount])
    clear_fields()

def calculate_profits():
    revenue_sheet = workbook.worksheet("Revenue").get_all_values()
    expense_sheet = workbook.worksheet("Expenses").get_all_values()
    
    revenue_df = pd.DataFrame(revenue_sheet[1:], columns=[col.strip() for col in revenue_sheet[0]])
    expense_df = pd.DataFrame(expense_sheet[1:], columns=[col.strip() for col in expense_sheet[0]])
    
    if 'Date' in revenue_df.columns:
        revenue_df['Date'] = pd.to_datetime(revenue_df['Date'])
    else:
        messagebox.showerror("Error", "'Date' column not found in revenue data.")
        return
    
    if 'Date' in expense_df.columns:
        expense_df['Date'] = pd.to_datetime(expense_df['Date'])
    else:
        messagebox.showerror("Error", "'Date' column not found in expense data.")
        return
    
    revenue_df['Total Revenue'] = pd.to_numeric(revenue_df['Total Revenue'], errors='coerce')
    expense_df['Amount'] = pd.to_numeric(expense_df['Amount'], errors='coerce')
    
    total_revenue = revenue_df.groupby(revenue_df['Date'].dt.to_period('D'))['Total Revenue'].sum()
    total_expense = expense_df.groupby(expense_df['Date'].dt.to_period('D'))['Amount'].sum()
    
    profit_df = total_revenue.subtract(total_expense, fill_value=0).reset_index()
    profit_df.columns = ['Day', 'Profit']
    profit_df['Day'] = profit_df['Day'].astype(str)
    
    profit_sheet = workbook.worksheet("Profit")
    profit_sheet.clear()
    profit_sheet.update([profit_df.columns.values.tolist()] + profit_df.values.tolist())
    messagebox.showinfo("Success", "Profit calculation updated successfully.")
    clear_fields()

# GUI setup
def add_revenue_ui():
    date = date_entry.get()
    product = product_entry.get()
    quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    add_revenue(product, quantity, price, date)

def add_expense_ui():
    date = expense_date_entry.get()
    expense_type = expense_type_entry.get()
    description = description_entry.get()
    amount = float(amount_entry.get())
    add_expense(expense_type, description, amount, date)

def clear_fields():
    date_entry.delete(0, tk.END)
    product_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    expense_date_entry.delete(0, tk.END)
    expense_type_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Business Tracker")
root.geometry("600x400")  # Set initial window size

# Revenue UI
tk.Label(root, text="Add Revenue").grid(row=0, column=0, columnspan=2)

tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=1, column=1)
date_entry.insert(0, "YYYY-MM-DD")

tk.Label(root, text="Product").grid(row=2, column=0)
product_entry = tk.Entry(root)
product_entry.grid(row=2, column=1)
product_entry.insert(0, "Product Name")

tk.Label(root, text="Quantity").grid(row=3, column=0)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=3, column=1)
quantity_entry.insert(0, "Quantity")

tk.Label(root, text="Price").grid(row=4, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=4, column=1)
price_entry.insert(0, "Price")

tk.Button(root, text="Add Revenue", command=add_revenue_ui).grid(row=5, column=0, columnspan=2)

# Expense UI
tk.Label(root, text="Add Expense").grid(row=6, column=0, columnspan=2)

tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=7, column=0)
expense_date_entry = tk.Entry(root)
expense_date_entry.grid(row=7, column=1)
expense_date_entry.insert(0, "YYYY-MM-DD")

tk.Label(root, text="Expense Type").grid(row=8, column=0)
expense_type_entry = tk.Entry(root)
expense_type_entry.grid(row=8, column=1)
expense_type_entry.insert(0, "Expense Type")

tk.Label(root, text="Description").grid(row=9, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=9, column=1)
description_entry.insert(0, "Description")

tk.Label(root, text="Amount").grid(row=10, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=10, column=1)
amount_entry.insert(0, "Amount")

tk.Button(root, text="Add Expense", command=add_expense_ui).grid(row=11, column=0, columnspan=2)

# Calculate Profits UI
tk.Button(root, text="Calculate Profits", command=calculate_profits).grid(row=12, column=0, columnspan=2)

# Clear Fields UI
tk.Button(root, text="Clear Fields", command=clear_fields).grid(row=13, column=0, columnspan=2)

root.mainloop()
