import gspread
import pandas as pd
import numpy as np

from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from googleapiclient import discovery
from pprint import pprint


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
SHEET = GSPREAD_CLIENT.open('Netflix Rotten Tomatoes Data')
service = discovery.build('sheets', 'v4', credentials=CREDS)

# The ID of the spreadsheet to update.
spreadsheet_id = '1v8fZd7UYTWa6Rt1QhaZ2gBqS0if6hP0KbOzWCR_r4mA'


def create_worksheet(worksheet_name):
    """
    This function create a new sheet in the Netflix Rotten Tomatoes spreadsheet
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
            sh = SHEET.worksheet(worksheet_name)
            sh.format("A1:AB1", {"horizontalAlignment": "CENTER", "textFormat": {"bold": True}})
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
        search_column = input("Please enter the column name on which you wish to filter the data: ")
        fetch_worksheet = SHEET.worksheet('Subset')
        column_list = fetch_worksheet.row_values(1)
        found = False
        col_cnt = 0
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
    """
    Function for catching errors
    """
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
    This data will be combined with the filter criteria to return valid
    rows from the sheet. A while loop is used to receive user input, the
    loop contiues until the user provides valid input.
    The rows of data fetched will be populated in "User Requested Data"
    """
    while True:
        try:
            user_input = []
            j = []
            user_input = input(f"Please enter the criteria to search in the {search_column} column: ")
            print("Searching for data...\n")
            i = user_input.split(' ')
            j.extend(i)
            if len(j) > 1:
                user_input = "|".join(j)

            fetch_worksheet = SHEET.worksheet('Subset')
            user_worksheet = SHEET.worksheet('User Requested Data')
            dataframe = pd.DataFrame(fetch_worksheet.get_all_records())
            user_select = dataframe[dataframe[search_column].str.contains(user_input, case=False, na=False)]
            set_with_dataframe(user_worksheet, user_select, include_column_header=True)
            print(f"{user_select.shape[0]} rows found")
            return True
        except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
            return False


def fetch_unique(duplicate_data):
    """
    Function creates a list of unique entries from every cell for the respect column
    """
    # Filter out duplicates from cells
    row_cnt = len(duplicate_data)
    new_data = ''
    for i in range(0, row_cnt):
        new_data = new_data + duplicate_data[i]
        if i != (row_cnt - 1):
            new_data = new_data + ','

    # Remove space before word
    i_temp = new_data.replace(', ', ',')
    # Remove double comma before word
    i_temp = i_temp.replace(',,', ',')

    # Convert string to list
    i_list = i_temp.split(',')

    # Convert list to set to remove duplicates
    i_set = set(i_list)

    # Convert set to list
    new_data = list(i_set)

    return sorted(new_data)


def get_statistics():
    """
    This function fetches unique entries from the
    'Title', 'Genre', 'Series or Movie', 'Director', 'Actors'
    columns and insert the results in the statistics worksheet
    """

    print("Preparing statistics data...")

    fetch_worksheet = SHEET.worksheet('Subset')
    stats_sheet = SHEET.worksheet('Statistics')
    column_headings = ['Title', 'Genre', 'Series or Movie', 'Director', 'Actors']
    dataframe = pd.DataFrame(fetch_worksheet.get_all_records(), columns=column_headings)

    # Get unique entries in column
    unique_title = dataframe['Title'].unique()
    unique_genre = dataframe['Genre'].unique()
    unique_series_movie = dataframe['Series or Movie'].unique()
    unique_director = dataframe['Director'].unique()
    unique_actor = dataframe['Actors'].unique()

    # Remove duplicate within cell of the column
    unique_genre = fetch_unique(unique_genre)
    unique_director = fetch_unique(unique_director)
    unique_actor = fetch_unique(unique_actor)

    cnt_title = len(unique_title)
    cnt_genre = len(unique_genre)
    cnt_series_movie = len(unique_series_movie)
    cnt_director = len(unique_director)
    cnt_actor = len(unique_actor)

    unique_count = (cnt_title, cnt_genre, cnt_series_movie, cnt_director, cnt_actor)
    row_cnt = max(unique_count) + 2

    # Insert the unique record count in the first row of the column
    unique_title = np.insert(unique_title, 0, cnt_title)
    unique_genre = np.insert(unique_genre, 0, cnt_genre)
    unique_series_movie = np.insert(unique_series_movie, 0, cnt_series_movie)
    unique_director = np.insert(unique_director, 0, cnt_director)
    unique_actor = np.insert(unique_actor, 0, cnt_actor)

    title_col = [*unique_title, *[''] * (row_cnt - len(unique_title))]
    genre_col = [*unique_genre, *[''] * (row_cnt - len(unique_genre))]
    series_movie_col = [*unique_series_movie, *[''] * (row_cnt - len(unique_series_movie))]
    director_col = [*unique_director, *[''] * (row_cnt - len(unique_director))]
    actor_col = [*unique_actor, *[''] * (row_cnt - len(unique_actor))]

    data_dict = {'Title': title_col, 'Genre': genre_col, 'Series and Movie': series_movie_col, 'Director': director_col, 'Actors': actor_col}
    new_df = pd.DataFrame.from_dict(data_dict)
    set_with_dataframe(stats_sheet, new_df, include_index=False)

    print(**************************************************)
    print(** You may review the Statistics worksheet for  **)
    print(** possible search criteria.                    **)
    print(**                                              **)
    print(** When you press Enter to continue, you will   **)
    print(** be prompted for search criteria.             **)
    print(**************************************************)

    input("Press Enter to continue...")


def main():
    """
    The main function. Runs all other functions.
    """
    print("************************************************************")
    print("*   Welcome to the Netflix Rotten Tomatoes data analysis!  *")
    print("************************************************************")
    create_worksheet("Statistics")
    create_worksheet('User Requested Data')
    print("************************************************************")
    get_statistics()
    get_header_choice()


main()
