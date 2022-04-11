![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome JPRodrigues-gh,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!

# Netflix Rotten Tomatoes dataset analysis

## Bugs and Fixes

* get_header_choice had endless while loop because return statement in validate_criteria Try statement was not inside the if statement. As a result validation would always be false and therefore get_data_choice would not be called.
  * Moved the validate_criteria Try statement inside the if statement
* get_data_choice call to validate_criteria placed in the for loop causing no rows found error to be shown on each row check. 
  * Moved the call to validate_criteria out of the for loop
* line 128 user_worksheet.append_row(column_list) passing incorrect argument 'column_list' instead of 'row_data'
* line 127 row_data = fetch_worksheet.row_values(i+1) had to +1 the argument to row_values as it returning a row before, not the requested row. 

## Sources and References

* The dataset I am using I downloaded from https://www.kaggle.com/datasets/ashishgup/netflix-rotten-tomatoes-metacritic-imdb
* https://www.w3schools.com/
* stackoverflow
* Google Sheets for Developers
* Youtube videos by Jie Jenn - Gsheet API help