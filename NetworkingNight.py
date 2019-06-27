# ----------------------------------------------------------------------------------------------------------------------
# Sophia Xu for UT's Society of Women Engineers
# This project is to assign students to their choosing of companies for SWE's annual Networking Night Dinner
# Project started: 6/19/2019
# ----------------------------------------------------------------------------------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------
# Connecting to the sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(credentials)
# ----------------------------------------------------------------------------------------------------------------------

# Get first sheet
students = client.open("Copy of 2018 SWE Networking Night Student Registration (Responses)").sheet1

companies = client.open("Copy of 2018 SWE Networking Night Student Registration (Responses)").get_worksheet(1)

# Convert Google Sheet into a list of dictionaries
# "get_all_records()" Returns a list of dictionaries, all of them having the contents of the spreadsheet’s with the head
# row as keys, And each of these dictionaries holding the contents of subsequent rows of cells as values.


# Convert the list of dictionaries into a data frame
students_df = pd.DataFrame(students.get_all_records())
companies_df = pd.DataFrame(companies.get_all_records())
# We only care about the Name, EID, Major, Year, Email, and the 5 preferences
# Delete multiple columns from the data frame
students_df = students_df.drop(["Timestamp","Your Organization","Where did you hear about this event?",
                                "Vegetarian Meal Required?","Please list any food allergies or dietary restrictions.",
                                "If you are a Junior or Senior BME please select which track you are in or plan on being in.",
                                "Confirmation","Additional Comments"],axis=1)

students_df.columns = ['First','Second','Third','Fourth','Fifth','E_mail','FirstName','LastName','Major','EID','Year']
companies_df.columns = ['Company','Entree','Dessert','Majors']

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(students_df.head())
# Set index of data to be by EID, so can access by loc later.
#students_df.set_index('EID',inplace = True)
companies_df.set_index('Company',inplace = True)
# Get index of the last value in dataframe
last = students_df.index[-1]
last += 1   # Increment by one because range(num) goes to num-1

# main for loop that goes through every student

for student in students_df.itertuples():
    first, second, third, fourth, fifth, e_mail, firstName, lastName, major, eID, year = student
    # Create a list of the student's preferences
    student_preferences = [first,second,third,fourth,fifth]
    # Clear matchFound flag
    matchFound = 0
    # for loop that finds combinations where the combinations that work
    for preference1 in student_preferences:
        for preference2 in student_preferences:
            if preference1 == preference2:
                continue
            elif matchFound == 1:
                continue
            else:
                company1 = companies_df.get_value(preference1, 'Entree')
                if company1 > 0:
                    company2 = companies_df.get_value(preference2, 'Dessert')
                    if company2 > 0:
                        # this means a successful match
                        matchFound == 1
                        # Update & store number of seats left
                        companies_df.at[preference1, 'Entree'] = company1 - 1
                        companies_df.at[preference2, 'Dessert'] = company2 - 1
                        # Store the students choices


    if matchFound == 0:
        # If a match is not found, first iterate through the different companies to find at least one match
        # STUDENT picks Entree, WE pick Dessert
        for preference in student_preferences:
            # Find companies that want that major for Dessert





# For each student: Grab five preferences and make it into a list to find the 2 combinations that work

# Once you have the 2 combinations that work, put Last Name, First Name, EID, Major, Year, Email and the 2 combinations
# that work into a dataframe
# LastName  FirstName   EID     Major   Year    Email   Entree  Dessert

# Put the successful matches into a dataframe
# I need to finish this later but I just realized that this has to be for each student. If you cannot find a successful
# (PERFECT) match for a student, you then need to do the force match section
