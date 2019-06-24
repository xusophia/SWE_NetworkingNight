#----------------------------------------------------------------------------------------------------------------------
# Sophia Xu for UT's Society of Women Engineers
# This project is to assign students to their choosing of companies for SWE's annual Networking Night Dinner
# Project started: 6/19/2019
#----------------------------------------------------------------------------------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd

#-----------------------------------------------------------------------------------------------------------------------
# Connecting to the sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(credentials)
#-----------------------------------------------------------------------------------------------------------------------

# Get first sheet
sheet = client.open("Copy of 2018 SWE Networking Night Student Registration (Responses)").sheet1

# Convert Google Sheet into a list of dictionaries
# "get_all_records()" Returns a list of dictionaries, all of them having the contents of the spreadsheet’s with the head
# row as keys, And each of these dictionaries holding the contents of subsequent rows of cells as values.
data = sheet.get_all_records()

# Convert the list of dictionaries into a data frame
dataframe = pd.DataFrame(sheet.get_all_records())

# We only care about the Name, EID, Major, Year, Email, and the 5 preferences
# Delete multiple columns from the dataframe
dataframe = dataframe.drop(["Timestamp","Your Organization","Where did you hear about this event?","Vegetarian Meal Required?",
                            "Please list any food allergies or dietary restrictions.",
                            "If you are a Junior or Senior BME please select which track you are in or plan on being in."], axis=1)
print(dataframe)

# For each student: Grab five preferences and make it into a list to find the 2 combinations that work
