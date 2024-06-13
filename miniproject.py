import gspread
from google.oauth2.service_account import Credentials
import json
import time

# Load the credentials JSON file
with open("credentials.json") as f:
    credentials_info = json.load(f)

# Define the scopes and create the credentials object
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)

# Authorize the client
client = gspread.authorize(creds)

# Open the Google Sheet by ID
sheet_id = "1PdyVHRxvrHVCLCfnnl5kslQatZ4e-ExYNZjE6qZXNZU"
workbook = client.open_by_key(sheet_id)

# Define values to populate the worksheet
values = [
    ["Name", "Price", "Quantity"],
    ["Basketball", 29.99, 1],
    ["Jeans", 39.99, 4],
    ["Soap", 7.99, 3],
]

# Get a list of existing worksheet titles
worksheet_titles = [worksheet.title for worksheet in workbook.worksheets()]

# Prompt the user for the name of the worksheet they want to access
new_worksheet_name = input("What spreadsheet would you like to access? ")

if new_worksheet_name in worksheet_titles:
    sheet = workbook.worksheet(new_worksheet_name)
else:
    create_worksheet = input(f"{new_worksheet_name} wasn't found, would you like to create it? (y/n): ")
    if create_worksheet.lower() == "y":
        sheet = workbook.add_worksheet(new_worksheet_name, rows=10, cols=10)
    else:
        print(f"{new_worksheet_name} was not created.")
        quit()

# Clear the existing content of the worksheet
sheet.clear()

# Update the worksheet with new values
sheet.update(f"A1:C{len(values)}", values)

print(f"Worksheet '{sheet.title}' has been updated with new values.")

sheet.update_cell(len(values)+1, 2, "=sum(B2:B4)")
sheet.update_cell(len(values)+1, 3, "=sum(C2:C4)")
#Make it bold
sheet.format("A1:C1", {"textFormat":{"bold": True}})

