# imports the entire gspread library which provides access to any function, class or method within it
# install gspread package -- pip3 install gspread google-auth
import gspread
# Import pandas library -- pip3 install pandas
import pandas as pd

# imports the Credentials class which is part of the service_account function from the Google auth library. 
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# The scope lists the APIs that the program should access in order to run.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"

# constant variable CREDS set by calling the from_service_account_file method
# of the Credentials class and passing it our creds.json file
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Netflix Rotten Tomatoes Analysis')

#  pip3 install google-api-python-client
from googleapiclient import discovery

service = discovery.build('sheets', 'v4', credentials=CREDS)

# The ID of the spreadsheet to update.
spreadsheet_id = '1v8fZd7UYTWa6Rt1QhaZ2gBqS0if6hP0KbOzWCR_r4mA'

# Write your code to expect a terminal of 80 characters wide and 24 rows high
def create_worksheet(worksheet_name):
    """
    This function will create a new sheet in the Netflix Rotten Tomatoes Analysis spreadsheet
    """
    try:
        # Check if the sheet exist, if so clear the contents
        # print(worksheet_name)
        if SHEET.worksheet(worksheet_name):
            print(f"Preparing {worksheet_name} worksheet")
            SHEET.worksheet(worksheet_name).clear()
    except Exception as e:
        # Sheet doesn't exist, create sheet
        print(f"Creating new {worksheet_name} worksheet ...")
        SHEET.add_worksheet(title=worksheet_name, rows=500, cols=28)
        #pip install gspread-formatting
        SHEET.worksheet(worksheet_name).format("A1:AB1", {"textFormat": {"bold": True}})
    

def get_header_choice():
    """
    The user is prompted for the filter criteria
    The number of rows affect will be printed to the screen
    A while loop is used to receive user input, the loop contiues until
    the user provides valid input
    The rows of data fetched will be populated in "User Requested Data"
    """
    get_data=False
    while True:
        print("You may search on the following columns: ")
        print("Title, Genre, Series or Movie, Director, Actors")
        print("(You may provide 1 column)")
        search_column = input("Please enter the column on which you wish to filter the data: ")
        fetch_worksheet = SHEET.worksheet('Subset')
        column_list = fetch_worksheet.row_values(1)
        found=False
        col_cnt=0
        data=''
        for i in column_list:
            col_cnt+=1
            if i == search_column:
               found=True
               col_idx=col_cnt
               break

        if validate_criteria(found, search_column, 'column'):
            get_data = True
            break

    if get_data:
        get_data_choice(search_column, col_idx)
    

def get_data_choice(search_column, col_idx):
    """
    The user is prompted for the data criteria
    This data will be combined with the filter criteria to return valid rows from the sheet
    A while loop is used to receive user input, the loop contiues until the user provides valid input
    The rows of data fetched will be populated in "User Requested Data"
    """
    while True:
        try:
            data = input(f"Please enter the data to search in the {search_column} column: ")
            print("Searching for data...\n")
            fetch_worksheet = SHEET.worksheet('Subset')
            row_cnt = len(fetch_worksheet.get_all_values())
            column = fetch_worksheet.col_values(col_idx)
 
            create_worksheet('User Requested Data')
            user_worksheet = SHEET.worksheet('User Requested Data')
            dataframe = pd.DataFrame(fetch_worksheet.get_all_records())
            user_select = dataframe[dataframe[search_column] == data]
            set_with_dataframe(user_worksheet, user_select, include_column_header=True)
            print(f"{user_select.shape[0]} rows found")
            return True
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
            return False
        

def validate_criteria(found, criteria, search):
    try:        
        if not found:
            if search=='column':
               raise ValueError(
                  f"'{criteria}' is not a valid option"
               )
            elif search=='data':
                raise ValueError(
                  f"No rows found containing '{criteria}'"
                )
            return False
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def main():
    """
    The main function. Runs all other functions.
    """
    create_worksheet("Statistics")
    get_header_choice()

print("Welcome to the Netflix Rotten Tomatoes data analysis!")
main()