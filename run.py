# imports the entire gspread library which provides access to any function, class or method within it
# install gspread package -- pip3 install gspread google-auth
import gspread
# imports the Credentials class which is part of the service_account function from the Google auth library. 
from google.oauth2.service_account import Credentials
# The scope lists the APIs that the program should access in order to run.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# constant variable CREDS set by calling the from_service_account_file method
# of the Credentials class and passing it our creds.json file
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Netflix Rotten Tomatoes Analysis')
# The above code I have taken from the Love Sandwiches project walk through

from googleapiclient import discovery

service = discovery.build('sheets', 'v4', credentials=CREDS)

# The ID of the spreadsheet to update.
spreadsheet_id = '1v8fZd7UYTWa6Rt1QhaZ2gBqS0if6hP0KbOzWCR_r4mA'  # TODO: Update placeholder value.

# The A1 notation of the values to clear.
range_ = 'User Requested Data'  # TODO: Update placeholder value.

# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Install pandas package --  pip3 install pandas
# Import pandas library 
# import pandas as pd

# dataSet = pd.read_csv('dataset/netflix-rotten-tomatoes-metacritic-imdb.csv')
# df = dataSet.copy()
# df.head()
# df.info()

# df2 = df[[column for column in df if df[column].count() / len(df) >= 0.3]]

# # del df2['Image']
# print("List of dropped columns:", end=" \n")
# for c in df.columns:
#     if c not in df2.columns:
#         print(c, end=", \n")
#         # del df2[c]
# df = df2
# df.info()

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
        # print(filter)
        fetch_worksheet = SHEET.worksheet('Subset')
        column_list = fetch_worksheet.row_values(1)
        found=False
        col_cnt=0
        data=''
        for i in column_list:
            # print(i)
            col_cnt+=1
            if i == search_column:
               found=True
               col_idx=col_cnt
            #    print(col_idx)
               break

        if validate_criteria(found, search_column):
            get_data = True
            # print(get_data)
            break

    if get_data:
        data = get_data_choice(search_column, col_idx)
    
    # print(search_column)
    # print(data)
    # print(col_idx)
    return search_column

def get_data_choice(search_column, col_idx):
    """
    The user is prompted for the data criteria
    This data will be combined with the filter criteria to return valid rows from the sheet
    A while loop is used to receive user input, the loop contiues until the user provides valid input
    The rows of data fetched will be populated in "User Requested Data"
    """
    while True:
        data = input(f"Please enter the data to search in the {search_column} column: ")
        fetch_worksheet = SHEET.worksheet('Subset')
        user_worksheet = SHEET.worksheet('User Requested Data')
        row_cnt = len(fetch_worksheet.get_all_values())
        # cell = fetch_worksheet.find(data, in_column=col_idx)
        column = fetch_worksheet.col_values(col_idx)

        cnt=0
        for i in range(1, 50):
            if data.lower() in column[i].lower():
                cnt+=1
                if cnt==1:
                   request = service.spreadsheets().values().clear(
                                     spreadsheetId=spreadsheet_id,
                                     range=range_)
                                      #, body=clear_values_request_body)
                   response = request.execute()
                   column_list = fetch_worksheet.row_values(1)
                   user_worksheet.append_row(column_list)

                # print(column[i])
            # user_worksheet.append_row(i)

        break
        # print(fetch_worksheet.cols)
        # found=False
        # for i in column_list:
        #     if i == search_column:
        #        found=True
        # validate_criteria(found, search_column)

    return search_column

def validate_criteria(found, criteria):
    try:        
        if not found:
            raise ValueError(
              f"{criteria} is not a valid option"
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
    search_column = get_header_choice()

print("Welcome to the Netflix Rotten Tomatoes data analysis!")
main()