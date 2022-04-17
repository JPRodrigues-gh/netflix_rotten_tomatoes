# Netflix Rotten Tomatoes dataset analysis

## User Stories

* The user is required to have a google account.
* The application begins by first creating a gsheet for the user
* The gsheet will contain 2 sheets, "Statistics" and "User Requested Data"
* The application will then populate the "Statistics" sheet with data relating to the first filter criteria:
  * Title, Genre, Series or Movie, Director, Actors
  * Below the headings there will be a count of the unique rows for the respective column
  * Data relating to the columns above will be drawn and manipulated from the gsheet containing the subset of data "Netflix Rotten Tomatoes"
* The user is then prompt for the first search criteria:
  * Title, Genre, Series or Movie, Director, Actors
* The next user prompt is for specific data

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


## Sources and References

* The dataset I am using I downloaded from https://www.kaggle.com/datasets/ashishgup/netflix-rotten-tomatoes-metacritic-imdb
* I the Love Sandwiches project walk through to set up my gspread and creds for the Google API 
* https://www.w3schools.com/
* stackoverflow
* Google Sheets for Developers
* pandas.pydata.org
* Youtube videos by Jie Jenn - Gsheet API help
