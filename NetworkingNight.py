# ----------------------------------------------------------------------------------------------------------------------
# Sophia Xu for UT's Society of Women Engineers
# This project is to assign students to their choosing of companies for SWE's annual Networking Night Dinner
# Project started: 6/19/2019
# ----------------------------------------------------------------------------------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
from collections import defaultdict

def Merge(*dict_args):
    assignments = {}
    for dictionary in dict_args:
        assignments.update(dictionary)
    return assignments
# ----------------------------------------------------------------------------------------------------------------------
# Connecting to the sheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(credentials)
# ----------------------------------------------------------------------------------------------------------------------

# Get first sheet - info on students
students = client.open("Copy of 2018 SWE Networking Night Student Registration (Responses)").sheet1
# Get second sheet - info on companies
companies = client.open("Copy of 2018 SWE Networking Night Student Registration (Responses)").get_worksheet(1)

# "get_all_records()" Returns a list of dictionaries, all of them having the contents of the spreadsheet’s with the head
# row as keys, And each of these dictionaries holding the contents of subsequent rows of cells as values.


# Convert the list of dictionaries into a data frame
students_df = pd.DataFrame(students.get_all_records())
companies_df = pd.DataFrame(companies.get_all_records())

# We only care about the Name, EID, Major, Year, Email, and the 5 preferences
# Delete columns that we don't use from the data frame
students_df = students_df.drop(["Timestamp","Your Organization","Where did you hear about this event?",
                                "Vegetarian Meal Required?","Please list any food allergies or dietary restrictions.",
                                "If you are a Junior or Senior BME please select which track you are in or plan on being in.",
                                "Confirmation","Additional Comments"],axis=1)
# Rename columns for ease of accessing with df
students_df.columns = ['First','Second','Third','Fourth','Fifth','E_mail','FirstName','LastName','Major','EID','Year']
companies_df.columns = ['Company','Entree','Dessert','Majors']

# Set index of companies df to be accessed by company name
companies_df.set_index('Company',inplace = True)
companies_df['Entree'] = companies_df['Entree'].astype(int)
companies_df['Dessert']= companies_df['Dessert'].astype(int)

# Create empty dictionaries to be appended later for matches found

firstName_dict = {}
firstName_dict['First Name:'] = []
lastName_dict = {}
lastName_dict['Last Name:'] = []
eID_dict = {}
eID_dict['EID:']=[]
year_dict = {}
year_dict['Year:']=[]
email_dict={}
email_dict['E-mail:']=[]
entree_dict = {}
entree_dict['Entree Seating:']=[]
dessert_dict = {}
dessert_dict['Dessert Seating:']=[]

# main: goes through each student (each row)
for student in students_df.itertuples():

    index, first, second, third, fourth, fifth, email, firstName, lastName, major, eID, year = student
    firstName_dict['First Name:'].append(firstName)
    lastName_dict['Last Name:'].append(lastName)
    eID_dict['EID:'].append(eID)
    year_dict['Year:'].append(year)
    email_dict['E-mail:'].append(email)
    # Create a list of the student's preferences
    student_preferences = [first,second,third,fourth,fifth]
    # Clear matchFound flag
    matchFound = 0
    co = company1 = companies_df.at['Accenture', 'Entree']
    # for loop that finds combinations where the combinations that work
    for preference1 in student_preferences:
        for preference2 in student_preferences:
            if preference1 == preference2:
                continue
            elif matchFound == 1:
                continue # may be a break
            else:
                company1 = companies_df.at[preference1, 'Entree']
                if company1 > 0:
                    company2 = companies_df.at[preference2, 'Dessert']
                    if company2 > 0:
                        # this means a successful match
                        matchFound = 1
                        # Update & store number of seats left
                        companies_df.at[preference1, 'Entree'] = companies_df.at[preference1, 'Entree'] - 1
                        companies_df.at[preference2, 'Dessert'] = companies_df.at[preference2, 'Dessert'] - 1
                        # Store the students choices into dictionary to be appended later in a dataframe
                        entree_dict['Entree Seating:'].append(preference1)
                        dessert_dict['Dessert Seating:'].append(preference2)
    print(len(firstName_dict['First Name:']))
    print(len(lastName_dict['Last Name:']))
    print(len(eID_dict['EID:']))
    print(len(year_dict['Year:']))
    print(len(email_dict['E-mail:']))
    print(len(entree_dict['Entree Seating:']))
    print(len(dessert_dict['Dessert Seating:']))
    print('*******************')
    if matchFound == 0:
        # If a match is not found, first iterate through the different companies to find at least one match
        # STUDENT picks Entree, WE pick Dessert
        for preference in student_preferences:
            findEntree_df = companies_df.loc[[preference]]
            findEntree_df = findEntree_df[findEntree_df['Entree'] > 0]
            if not findEntree_df.empty:
                # Find companies that want that major for Dessert
                # Need to search by matching string for majors + open spots
                pickDessert_df = companies_df[(companies_df['Majors'].str.contains(major)) & (companies_df['Dessert'] > 0)]
                if not pickDessert_df.empty:
                    # Update & store number of seats left
                    companies_df.at[preference, 'Entree'] = companies_df.at[preference, 'Entree'] - 1
                    dessert_co_labels = pickDessert_df.axes[0].tolist()
                    dessert_company = dessert_co_labels[0]
                    companies_df.at[dessert_company, 'Dessert'] = companies_df.at[dessert_company, 'Dessert'] - 1
                    entree_dict['Entree Seating:'].append(preference)
                    dessert_dict['Dessert Seating:'].append(dessert_company)
                    print(len(entree_dict['Entree Seating:']))
                    print(len(dessert_dict['Dessert Seating:']))
                    print('----------------------')
                    matchFound = 1
                else:
                    # If match if not found, now STUDENT picks Dessert, WE pick Entree
                    for preference in student_preferences:
                        findDessert_df = companies_df.loc[[preference]]
                        findDessert_df = findDessert_df[findDessert_df['Dessert'] > 0]
                        if not findDessert_df.empty:
                            pickEntree_df = companies_df[(companies_df['Majors'].str.contains(major)) & companies_df['Entree'].between(1,7)]
                            if not pickEntree_df.empty:
                                companies_df.at[preference,'Dessert']=companies_df.at[preference,'Dessert'] - 1
                                entree_co_labels = pickEntree_df.axes[0].tolist()
                                entree_company = entree_co_labels[0]
                                companies_df.at[entree_company,'Entree'] = companies_df.at[entree_company,'Entree'] - 1
                                entree_dict['Entree Seating:'].append(entree_company)
                                dessert_dict['Dessert Seating:'].append(preference)
                                print(len(entree_dict['Entree Seating:']))
                                print(len(dessert_dict['Dessert Seating:']))
                                print('^^^^^^^^^^^^^^^^^^^^^^^^')
                            else: # all solutions have failed
                                entree_dict['Entree Seating:'].append("failed")
                                dessert_dict['Dessert Seating:'].append("failed")
                                print(len(entree_dict['Entree Seating:']))
                                print(len(dessert_dict['Dessert Seating:']))
                                print('+++++++++++++++++++++++')


# Now, Combine all of the dictionaries created into a data frame
assignments = Merge(firstName_dict, lastName_dict, eID_dict,year_dict,email_dict,entree_dict, dessert_dict)
print(len(firstName_dict['First Name:']))
print(len(lastName_dict['Last Name:']))
print(len(eID_dict['EID:']))
print(len(year_dict['Year:']))
print(len(email_dict['E-mail:']))
print(len(entree_dict['Entree Seating:']))
print(len(dessert_dict['Dessert Seating:']))
#assignments_df = pd.DataFrame(assignments)


# For each student: Grab five preferences and make it into a list to find the 2 combinations that work

# Once you have the 2 combinations that work, put Last Name, First Name, EID, Major, Year, Email and the 2 combinations
# that work into a dataframe
# LastName  FirstName   EID     Major   Year    Email   Entree  Dessert

# Put the successful matches into a dataframe
# I need to finish this later but I just realized that this has to be for each student. If you cannot find a successful
# (PERFECT) match for a student, you then need to do the force match section

