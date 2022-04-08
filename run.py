# Your code goes here.
# You can delete these comments, but do not change the name of this file

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
# The above I have taken from the Love Sandwiches project walk through

# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Install pandas package --  pip3 install pandas
# Import pandas library 
import pandas as pandas
dataSet = pandas.read_csv('dataset/netflix-rotten-tomatoes-metacritic-imdb.csv')
df = dataSet.copy()
df.head()
df.info()