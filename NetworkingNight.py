# ----------------------------------------------------------------------------------------------------------------------
# Sophia Xu for UT's Society of Women Engineers
# This project is to assign students to their choosing of companies for SWE's annual Networking Night Dinner
# Project started: 6/19/2019
# ----------------------------------------------------------------------------------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import xlsxwriter
from collections import defaultdict
import gspread_dataframe as gd
from matplotlib import pyplot as plt


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
major_dict={}
major_dict['Major:']=[]
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

preference_entree_dict = {}
preference_entree_dict['Entree Preference']=[]
preference_dessert_dict={}
preference_dessert_dict['Dessert Preference']=[]

# main: goes through each student (each row)
for student in students_df.itertuples():

    index, first, second, third, fourth, fifth, email, firstName, lastName, major, eID, year = student
    firstName_dict['First Name:'].append(firstName)
    lastName_dict['Last Name:'].append(lastName)
    eID_dict['EID:'].append(eID)
    year_dict['Year:'].append(year)
    email_dict['E-mail:'].append(email)
    major_dict['Major:'].append(major)
    # Create a list of the student's preferences
    student_preferences = [first,second,third,fourth,fifth]
    # Clear matchFound flag
    matchFound = 0

    # for loop that finds combinations where the combinations that work
    for entree, preference1 in enumerate(student_preferences, 1):
        for dessert, preference2 in enumerate(student_preferences, 1):
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
                        preference_entree_dict['Entree Preference'].append(entree)
                        preference_dessert_dict['Dessert Preference'].append(dessert)
                        # Store the students choices into dictionary to be appended later in a dataframe
                        entree_dict['Entree Seating:'].append(preference1)
                        dessert_dict['Dessert Seating:'].append(preference2)

    if matchFound == 0:
        # If a match is not found, first iterate through the different companies to find at least one match
        # STUDENT picks Entree, WE pick Dessert
        for preference in student_preferences:
            findEntree_df = companies_df.loc[[preference]]
            findEntree_df = findEntree_df[findEntree_df['Entree'] > 0]
            if not findEntree_df.empty & matchFound != 1:
                # Find companies that want that major for Dessert
                # Need to search by matching string for majors + open spots
                pickDessert_df = companies_df[(companies_df['Majors'].str.contains(major)) & (companies_df['Dessert'] > 0)]
                if not pickDessert_df.empty:
                    # Update & store number of seats left

                    companies_df.loc[preference, 'Entree'] = companies_df.at[preference, 'Entree'] - 1
                    dessert_co_labels = pickDessert_df.axes[0].tolist()
                    dessert_company = dessert_co_labels[0]
                    companies_df.loc[dessert_company, 'Dessert'] = companies_df.at[dessert_company, 'Dessert'] - 1
                    entree_dict['Entree Seating:'].append(preference)
                    dessert_dict['Dessert Seating:'].append(dessert_company)

                    matchFound = 1
    if matchFound == 0:
        for preference in student_preferences:
            findDessert_df = companies_df.loc[[preference]]
            findDessert_df = findDessert_df[findDessert_df['Dessert'] > 0]
            if (not findDessert_df.empty) & (matchFound != 1):
                pickEntree_df = companies_df[(companies_df['Majors'].str.contains(major)) & companies_df['Entree'].between(1,7)]
                if not pickEntree_df.empty:
                    companies_df.loc[preference,'Dessert'] = companies_df.loc[preference,'Dessert'] - 1
                    entree_co_labels = pickEntree_df.axes[0].tolist()
                    entree_company = entree_co_labels[0]
                    companies_df.loc[entree_company,'Entree'] = companies_df.at[entree_company,'Entree'] - 1
                    entree_dict['Entree Seating:'].append(entree_company)
                    dessert_dict['Dessert Seating:'].append(preference)

                    matchFound = 1
    if matchFound == 0: # all solutions have failed
        entree_dict['Entree Seating:'].append("failed")
        dessert_dict['Dessert Seating:'].append("failed")



# Now, Combine all of the dictionaries created into a data frame
results = Merge(firstName_dict, lastName_dict, eID_dict,year_dict,email_dict,entree_dict, dessert_dict, major_dict)
results_df = pd.DataFrame(results)

# Create a data frame of only the successful assignments
assignments_df = results_df[~((results_df['Entree Seating:'].str.contains('failed')))]

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('Results_2018.xlsx', engine='xlsxwriter')

# Convert the assignments dataframe to an XlsxWriter Excel object.
results_df.to_excel(writer, sheet_name='Sheet1')
assignments_df.to_excel(writer, sheet_name = 'Sheet2')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

# Analysis of results

# Analyze the preference number people got
analysis = Merge(preference_entree_dict,preference_dessert_dict)
analysis_df = pd.DataFrame(analysis)
analysis_df.hist(column = ['Dessert Preference', 'Entree Preference'])
plt.savefig('preferences.png')

# Analyze the distribution of majors
assignments_df[['Major:']].apply(pd.value_counts).plot(kind = 'bar')
plt.yticks(fontsize = 10)
plt.xticks(fontsize=4, rotation = 35)
plt.title('Successful Assignments: Major Distribution')
plt.savefig('Major_Distribution.png', dpi = 1000)
results_df[['Major:']].apply(pd.value_counts).plot(kind = 'bar')
plt.xticks(fontsize = 6)
plt.title('ALL: Major Distribution')
plt.gcf().subplots_adjust(bottom = 0.35)
plt.savefig('Major_Distribution_ALL.png', dpi = 1000)
# Analyze the distribution of years
assignments_df[['Year:']].apply(pd.value_counts).plot(kind='bar')
plt.xticks(fontsize = 9, rotation = 25)
plt.title('Successful Assignments: Year Distribution')
plt.savefig('Year_Distribution.png', dpi = 1000)
#Need to analyze the distribution of years of the succesful assignments vs total
results_df[['Year:']].apply(pd.value_counts).plot(kind = 'bar')
plt.xticks(fontsize = 6, rotation = 45)
plt.title('All: Year Distribution')
plt.savefig('Year_Distribution_ALL.png', dpi = 1000)



# Create a histogram

# Once you have the 2 combinations that work, put Last Name, First Name, EID, Major, Year, Email and the 2 combinations
# that work into a dataframe
# LastName  FirstName   EID     Major   Year    Email   Entree  Dessert

# Put the successful matches into a dataframe
# I need to finish this later but I just realized that this has to be for each student. If you cannot find a successful
# (PERFECT) match for a student, you then need to do the force match section

