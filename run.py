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

def get_user_input():
    """
    The user is prompted for the filter criteria
    The number of rows affect will be printed to the screen
    A while loop is used to receive user input, the loop contiues until
    the user provides valid input
    The rows of data fetched will be populated in "User Requested Data"
    """
    filter = []
    while True:
        print("You may search on the following columns: ")
        print("Title, Genre, Serie or Movie, Director, Actors")
        print("(You may provide 1 column)")
        filter = input("Please enter the column on which you wish to filter the data: ")

        if validate_criteria(filter):
        #    print(filter)
           break

    return filter
   
def validate_criteria(criteria):
    try:
        fetch_worksheet = SHEET.worksheet('Subset')
        column_list = fetch_worksheet.row_values(1)
        for i in column_list:
            if i == criteria:
               print(i)
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def main():
    """
    The main function. Runs all other functions.
    """
    filter = get_user_input()

print("Welcome to the Netflix Rotten Tomatoes data analysis!")
main()