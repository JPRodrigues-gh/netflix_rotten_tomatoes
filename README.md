# Netflix Rotten Tomatoes dataset analysis


## Introduction 

The app provides the user with a sheet containing a subset of data from the Netflix Rotten Tomatoes dataset obtained from https://www.kaggle.com/datasets/ashishgup/netflix-rotten-tomatoes-metacritic-imdb. The app presents the user with data stastics from which the user may gain insight into potential search options relating to Netflix Rotten Tomatoes Series and Movies.


## App Function and User Stories

* The user is required to have a google account.
* The app makes use of the "Netflix Rotten Tomatoes Data" sheet:
  * https://docs.google.com/spreadsheets/d/1v8fZd7UYTWa6Rt1QhaZ2gBqS0if6hP0KbOzWCR_r4mA/edit#gid=0

  ![image](https://user-images.githubusercontent.com/22208203/163705176-fecf6b4c-3eb6-4de8-a5bf-55ff9cd3d350.png)

* The application begins by checking if the "Statistics" and "User Requested Data" exist.
  * If they do not exist they are created
  * If they do exist they are cleared of any data

  ![image](https://user-images.githubusercontent.com/22208203/163705112-2c6c40a3-bb5c-48b6-ad90-b2f9c4ce2e4b.png)

* Next the application will populate the "Statistics" worksheet with data as follows:
  * Title, Genre, Series or Movie, Director, Actors column headings are added
  * Below the headings there will be a count of the unique rows for the respective column
  * Next, unique data, relating to the columns above, will be drawn and manipulated from the gsheet containing the subset of data 
    "Netflix Rotten Tomatoes" and set int this worksheet.
  
  ![image](https://user-images.githubusercontent.com/22208203/163705202-14815efd-b0bc-4ac0-84b8-cc0744f2fbd9.png)
    
* The user is then advised that they can use the "Statistics" worksheet to get an idea of what search data is available
* On pressing enter the user is prompted for the first search criteria:
  * Title, Genre, Series or Movie, Director, Actors
  * "Please enter the column name on which you wish to filter the data: \n"
* The next user prompt is for specific data relating to the headings
  * "Please enter the criteria to search in the {"Title" or "Genre" or "Series or Movie" or "Director" or "Actors"} column: \n"

  ![image](https://user-images.githubusercontent.com/22208203/163705296-cfbd29fd-13fb-48de-a09c-597b6bc6c98f.png)

  ![image](https://user-images.githubusercontent.com/22208203/163705537-13a4b674-8a47-410a-bd70-a61f87afdacb.png)

  ![image](https://user-images.githubusercontent.com/22208203/163705431-6f9d5c36-2a64-40ff-a8ae-29f75b56ff0f.png)

  ![image](https://user-images.githubusercontent.com/22208203/163705455-cdbe303f-b4fb-492a-a370-cc946e095836.png)


## Design

* I used Lucidchart to build a flow chart for the building the app

  ![image](https://user-images.githubusercontent.com/22208203/163698554-4ce56481-cf32-4e3a-8eaf-b5bb41b137e2.png)


## Features

* The console conatining the user interface
  

* The Netflix Rotten Tomatoes Data sheet
  
  * Link to the gsheet: https://docs.google.com/spreadsheets/d/1v8fZd7UYTWa6Rt1QhaZ2gBqS0if6hP0KbOzWCR_r4mA/edit#gid=1659555094


  ![image](https://user-images.githubusercontent.com/22208203/163698696-f9d20842-dd45-4ea3-b9d3-7066fa9e8a0b.png)

  ![image](https://user-images.githubusercontent.com/22208203/163698647-ed5e4f85-bfda-4de4-88b3-24111c5cf378.png)

  ![image](https://user-images.githubusercontent.com/22208203/163698840-860107d0-87ac-425a-84f0-7c3622726a15.png)


## Technologies Used

* Python
* GitHub
* GitPod
* Heroku
* Gsheets
* Google API
* Pandas
* Numpy
* Lucidchart


## Testing

* Passed the code through PEP8 linter and confirmed there are no problems
  ![image](https://user-images.githubusercontent.com/22208203/163696567-4139f709-c744-4541-bd8a-1d1f7b60523c.png)
* On program run, verified that the "Statistics" and "User Requested Data" worksheets are being created if they
  do not exist or cleared if they do exist
* Verified that the "Statistics" worksheet is being populated with unique values for columns Title, Genre,
  Series or Movie, Director, Actors respectively
* The user may use the data in the Statistics worksheet to establish possible search criteria
* For the first prompt tested for invalid input. User may only enter 1 of the column headings:
  * Title, Genre, Series or Movie, Director, Actors
  * Program was passed testing for input that was not an exact match for one of the headings
* For the second prompts the user for criteria that may be an exact or paertial match applying the combination of
  this input criteria and the Heading selected in the first prompt.
  * If no data found return message "No rows found".
  * The only exception to the above is if a user searches on the Actors column. Here the user should provide the
    exact name and suname of the actor
* Verified that the "User Requested Data" has been populated with data that fits the user's search criteria


## Bugs and Fixes

* get_header_choice had endless while loop because return statement in validate_criteria Try statement was not inside the if statement. As a result validation would always be false and therefore get_data_choice would not be called.
  * Moved the validate_criteria Try statement inside the if statement
* get_data_choice call to validate_criteria placed in the for loop causing no rows found error to be shown on each row check. 
  * Moved the call to validate_criteria out of the for loop
* line 128 user_worksheet.append_row(column_list) passing incorrect argument 'column_list' instead of 'row_data'
* line 127 row_data = fetch_worksheet.row_values(i+1) had to +1 the argument to row_values as it returning a row before, not the requested row.
* line 95 - increased the column range to AB. As a result the whole sheet was set to bold. Changes it to AB1.
* Quota exceeded error due to reads per minute. Changed to use pandas dataframes
  * gspread.exceptions.APIError: {'code': 429, 'message': "Quota exceeded for quota metric 'Read requests' and limit 'Read 
    requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:199256788443'.", 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'RATE_LIMIT_EXCEEDED', 'domain': 'googleapis.com', 'metadata': {'service': 'sheets.googleapis.com', 'consumer': 'projects/199256788443', 'quota_metric': 'sheets.googleapis.com/read_requests', 'quota_limit': 'ReadRequestsPerMinutePerUser'}}]}
* Bug in get_statistics() function throws an error
  * raise ValueError("All arrays must be of the same length")  ValueError: All arrays must be of the same length
  * padding the lists to the number of rows in the original source was failing because once the all the data unique actors were  
    listed the count exceeded the number of original rows in the source sheet.
  * Fixed by getting the count of the largest list of data
* Using new_df.loc[0] = unique_count in get_statistics was removing the first row of data.
  * Instead, I inserted the count in the respective lists before padding with empty string
* Due to adding of the count to the lists this affected the length of the lists.
  * I added 2 to the row_cnt to resolve the issue
* NOT really a bug, more of a nuisance
  * When searching for Actors the search method would search for the occurance of either of an Actor's name or surname, also in 
    part. eg. 'Liam Neeson' would also return Actors with name 'William' because liam appears in the name.
  * Solution was to place the code with and conditional statement where if the search is on Actors the method is not used. 


## Sources and References

* The dataset I am using I downloaded from https://www.kaggle.com/datasets/ashishgup/netflix-rotten-tomatoes-metacritic-imdb
* I the Love Sandwiches project walk through to set up my gspread and creds for the Google API 
* https://www.w3schools.com/
* stackoverflow
* python.org
* thispointer.com
* Google Sheets for Developers
* gspread.org
* pandas.pydata.org
* numpy.org
* Youtube videos by Jie Jenn - Gsheet API help


## Deployement

* The link to the deployed app:

  * https://netflix-rotten-tomatoes.herokuapp.com/
  
* Followed the following instruction from kevin_ci:

  ![image](https://user-images.githubusercontent.com/22208203/163704546-13b9f670-dec8-45eb-9e23-6d68a5247f7e.png)

* The app was deployed via the GitPod console.

  ![image](https://user-images.githubusercontent.com/22208203/163704510-63568164-4e21-4704-9165-2228f8ff91e5.png)
