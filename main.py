import gspread
from google.oauth2.service_account import Credentials
import json
import time

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# Load the credentials JSON file
with open("credentials.json") as f:
    credentials_info = json.load(f)

# Create the credentials object
creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)

# Authorize the client
client = gspread.authorize(creds)

# Open the Google Sheet by ID
sheet_id = "1PdyVHRxvrHVCLCfnnl5kslQatZ4e-ExYNZjE6qZXNZU"
workbook = client.open_by_key(sheet_id)


#Delete a worksheet
"""
worksheet_name = input("Enter the name of the worksheet to be deleted: ")
try:
    # Find the worksheet by name
    worksheet = workbook.worksheet(worksheet_name)
    workbook.del_worksheet(worksheet)
    time.sleep(0.7)
    print(f"{worksheet_name} has been deleted.")
    
except gspread.exceptions.WorksheetNotFound:
    # Handle the case where the worksheet is not found
    print(f"Worksheet '{worksheet_name}' not found.")
"""

#Sharing a Spreadsheet
"""
user_share = input("Enter the email address of the user you want to share the spreadsheet with: ")
role = input("What would be their role? (writer, commenter, reader): ")
sheet.share(user_share, perm_type = "user", role=role)
print(f"Spreadsheet shared with {user_share} with role {role}")
"""

#Basic Formatting
"""
#Make it bold
sheet.format("A1", {"textFormat":{"bold": True}})

#Background color
sheet.format("A1", {
    "backgroundColor": {
        "red": 1,
        "green": 0.9,
        "blue": 0.9
    }
})
"""

#Get location of cell with text
"""
value_to_find = input("Enter the value you want to find: ")
cell = sheet.find(value_to_find)
# Check if the cell is found
if cell is not None:
    print(f"{cell.value} was found in row {cell.row}, and column {cell.col}")
else:
    # Handle the case where the value couldn't be found
    print(f"The value '{value_to_find}' could not be found in the sheet.")
"""



#Get value of a cell
"""
#Use acell for boxes and shit
value = sheet.acell("A1").value
print(value)
"""

#Update cells
"""
col = int(input("Enter the col #: "))
row = int(input("Enter the row #: "))
# Get the current cell value
current_cell = sheet.cell(row, col).value
print(f"Column #{col} and row #{row} has the text of: {current_cell}")
# Get user input for the new cell value
user_text = input("What do you want to change it to? ")
print(f"Updated to: {user_text}")
# Update the cell with the new value
sheet.update_cell(row, col, user_text)
"""


#Changing Sheet title
"""
current_title = sheet.title
print(f"Current Title: {current_title}")
user_input = input("What do you want to update the title name to: ")
sheet.update_title(user_input)
print(f"Title updated to: {user_input}")
"""


#See titles of sheets
#sheets = map(lambda x: x.title, workbook.worksheets())
#print(list(sheets))

# Get the values from the first row
#values_list = workbook.sheet1.row_values(1)
#print(values_list)
