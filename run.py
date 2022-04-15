import gspread
import pandas as pd
import numpy as np
import pprint
from pprint import pprint
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from googleapiclient import discovery
from numpy import array, hstack, vstack

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
service = discovery.build('sheets', 'v4', credentials=CREDS)

# The ID of the spreadsheet to update.
spreadsheet_id = '1v8fZd7UYTWa6Rt1QhaZ2gBqS0if6hP0KbOzWCR_r4mA'

# Write your code to expect a terminal of 80 characters wide and 24 rows high
def create_worksheet(worksheet_name):
    """
    This function will create a new sheet in the Netflix Rotten Tomatoes spreadsheet
    """
    try:
        # Check if the sheet exist, if so clear the contents
        if SHEET.worksheet(worksheet_name):
            print(f"Preparing {worksheet_name} worksheet ...")
            SHEET.worksheet(worksheet_name).clear()
    except Exception:
        try:
            # Sheet doesn't exist, create sheet
            print(f"Creating new {worksheet_name} worksheet ...")
            SHEET.add_worksheet(title=worksheet_name, rows=500, cols=28)
            SHEET.worksheet(worksheet_name).format("A1:AB1", {"textFormat": {"bold": True}})
        except Exception as e:
            print(f"{e}")
            return False
    

def get_header_choice():
    """
    The user is prompted for the filter criteria
    The number of rows affect will be printed to the screen
    A while loop is used to receive user input, the loop contiues until
    the user provides valid input
    The rows of data fetched will be populated in "User Requested Data"
    """
    get_data = False
    while True:
        print("You may search on the following columns: ")
        print("Title, Genre, Series or Movie, Director, Actors")
        print("(You may provide 1 column)")
        search_column = input("Please enter the column on which you wish to filter the data: ")
        fetch_worksheet = SHEET.worksheet('Subset')
        column_list = fetch_worksheet.row_values(1)
        found = False
        col_cnt = 0
        data = ''
        for i in column_list:
            col_cnt += 1
            if i == search_column:
               found = True
               break

        if validate_criteria(found, search_column, 'column'):
            get_data = True
            break

    if get_data:
        get_data_choice(search_column)
 

def validate_criteria(found, criteria, search):
    try:        
        if not found:
            if search == 'column':
               raise ValueError(
                  f"'{criteria}' is not a valid option"
               )
            elif search == 'data':
                raise ValueError(
                  f"No rows found containing '{criteria}'"
                )
            return False
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def get_data_choice(search_column):
    """
    The user is prompted for the data criteria
    This data will be combined with the filter criteria to return valid rows from the sheet
    A while loop is used to receive user input, the loop contiues until the user provides valid input
    The rows of data fetched will be populated in "User Requested Data"
    """
    while True:
        try:
            user_input = []
            j = []
            user_input = input(f"Please enter the data to search in the {search_column} column: ")
            print("Searching for data...\n")
            i = user_input.split(' ')
            j.extend(i)
            if len(j)>1:
                user_input = "|".join(j)

            fetch_worksheet = SHEET.worksheet('Subset')
            user_worksheet = SHEET.worksheet('User Requested Data')
            dataframe = pd.DataFrame(fetch_worksheet.get_all_records())
            user_select = dataframe[dataframe[search_column].str.contains(user_input,case=False,na=False)]
            set_with_dataframe(user_worksheet, user_select, include_column_header=True)
            print(f"{user_select.shape[0]} rows found")
            return True
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
            return False
        
def get_statistics():
    fetch_worksheet = SHEET.worksheet('Subset')
    stats_sheet =  SHEET.worksheet('Statistics')
    column_headings = ['Title','Genre','Series or Movie','Director','Actors']
    row_cnt = len(fetch_worksheet.get_all_values())
    dataframe = pd.DataFrame(fetch_worksheet.get_all_records(), columns=['Title','Genre','Series or Movie','Director','Actors'])
    # pprint(dataframe)
    unique_count = []
    unique_title = dataframe['Title'].nunique()
    unique_genre = dataframe['Genre'].nunique()
    unique_series_movie = dataframe['Series or Movie'].nunique()
    unique_director = dataframe['Director'].nunique()
    unique_actors = dataframe['Actors'].nunique()
    unique_count.append(unique_title)
    unique_count.append(unique_genre)
    unique_count.append(unique_series_movie)
    unique_count.append(unique_director)
    unique_count.append(unique_actors)
    # pprint(unique_genre)
    # pprint(unique_series_movie)
    # pprint(unique_director)
    # pprint(unique_data)
    unique_titles = dataframe['Title'].unique()
    unique_genres = dataframe['Genre'].unique()
    unique_series_movie_s = dataframe['Series or Movie'].unique()
    unique_directors = dataframe['Director'].unique()
    unique_actorss = dataframe['Actors'].unique()

    unique_titles = [*unique_titles,*[''] * (row_cnt - len(unique_titles))]
    unique_titles = {unique_title: unique_titles}
    unique_genres = [*unique_genres,*[''] * (row_cnt - len(unique_genres))]
    unique_genres = {unique_genre: unique_genres}
    unique_series_movie_s = [*unique_series_movie_s,*[''] * (row_cnt - len(unique_series_movie_s))]
    unique_series_movie_s = {unique_series_movie: unique_series_movie_s}
    unique_directors = [*unique_directors,*[''] * (row_cnt - len(unique_directors))]
    unique_directors = {unique_director: unique_directors}
    unique_actorss = [*unique_actorss,*[''] * (row_cnt - len(unique_actorss))]
    unique_actorss = {unique_actors: unique_actorss}
    new_array = hstack([unique_titles,unique_genres,unique_series_movie_s,unique_directors,unique_actorss])
    # convert numpy array to dictionary
    # new_array = dict(enumerate(new_array.flatten(), 1))
    # pprint(new_array)
    new_df = pd.DataFrame(new_array)
    # pprint(new_df)
    # print("*********************************************************")
    stats_sheet.append_row(column_headings)
    stats_sheet.append_row(unique_count)
    set_with_dataframe(stats_sheet, new_df, include_index = False, row=3)
    input("Press Enter to continue...")


def main():
    """
    The main function. Runs all other functions.
    """
    print("*********************************************************")
    print("* Welcome to the Netflix Rotten Tomatoes data analysis! *")
    print("*********************************************************")
    create_worksheet("Statistics")
    create_worksheet('User Requested Data')
    print("*********************************************************")
    get_statistics()
    get_header_choice()


main()