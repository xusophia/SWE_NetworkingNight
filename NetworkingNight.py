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

#print(dataframe)
