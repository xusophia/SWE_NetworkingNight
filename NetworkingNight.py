# ----------------------------------------------------------------------------------------------------------------------
# Sophia Xu for UT's Society of Women Engineers
# This project is to assign students to their choosing of companies for SWE's annual Networking Night Dinner
# Project started: 6/19/2019
# ----------------------------------------------------------------------------------------------------------------------

import GSheets_Auth

import pandas as pd
from pprint import pprint

import xlsxwriter
from collections import defaultdict
import gspread_dataframe as gd
from matplotlib import pyplot as plt

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
# Analysis empty dictionaries
preference_entree_dict = {}
preference_entree_dict['Entree Preference']=[]
preference_dessert_dict={}
preference_dessert_dict['Dessert Preference']=[]


def Merge(*dict_args):
    assignments = {}
    for dictionary in dict_args:
        assignments.update(dictionary)
    return assignments

def dataFrameCleanup():
    # Rename columns for ease of accessing with df
    students_df.columns = ['First','Second','Third','Fourth','Fifth','E_mail','FirstName','LastName','Major','EID','Year']
    companies_df.columns = ['Company','Entree','Dessert','Majors']
    # Set index of companies df to be accessed by company name
    companies_df.set_index('Company',inplace = True)
    companies_df['Entree'] = companies_df['Entree'].astype(int)
    companies_df['Dessert']= companies_df['Dessert'].astype(int)
def appendStudentInfo(firstName, lastName, eID, year, email, major):
    firstName_dict['First Name:'].append(firstName)
    lastName_dict['Last Name:'].append(lastName)
    eID_dict['EID:'].append(eID)
    year_dict['Year:'].append(year)
    email_dict['E-mail:'].append(email)
    major_dict['Major:'].append(major)
def matchFoundUpdate(entree_co, dinner_co):
    # Update & store number of seats left
    companies_df.at[entree_co, 'Entree'] = companies_df.at[entree_co, 'Entree'] - 1
    companies_df.at[dinner_co, 'Dessert'] = companies_df.at[dinner_co, 'Dessert'] - 1

    # Store the students choices into dictionary to be appended later in a dataframe
    entree_dict['Entree Seating:'].append(entree_co)
    dessert_dict['Dessert Seating:'].append(dinner_co)
listToDrop = ["Timestamp","Your Organization","Where did you hear about this event?",
              "Vegetarian Meal Required?","Please list any food allergies or dietary restrictions.",
              "If you are a Junior or Senior BME please select which track you are in or plan on being in.",
              "Confirmation","Additional Comments"]
if __name__ == '__main__':
    # need to print some thing
    students, companies = GSheets_Auth.open_user_sheets("Copy of 2018 SWE Networking Night Student Registration (Responses)")
    # Convert the list of dictionaries into a data frame
    students_df = pd.DataFrame(students.get_all_records())
    companies_df = pd.DataFrame(companies.get_all_records())
    # We only care about the Name, EID, Major, Year, Email, and the 5 preferences
    # Delete columns that we don't use from the data frame
    students_df = students_df.drop(listToDrop, axis = 1)
    dataFrameCleanup()
    for student in students_df.itertuples():
        index, first, second, third, fourth, fifth, email, firstName, lastName, major, eID, year = student
        appendStudentInfo(firstName, lastName, eID, year, email, major)
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
                            matchFoundUpdate(preference1, preference2)
                            # This is for later analysis
                            preference_entree_dict['Entree Preference'].append(entree)
                            preference_dessert_dict['Dessert Preference'].append(dessert)
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
                        dessert_co_labels = pickDessert_df.axes[0].tolist()
                        dessert_company = dessert_co_labels[0]
                        matchFoundUpdate(preference, dessert_company)
                        matchFound = 1
        if matchFound == 0:
            for preference in student_preferences:
                findDessert_df = companies_df.loc[[preference]]
                findDessert_df = findDessert_df[findDessert_df['Dessert'] > 0]
                if (not findDessert_df.empty) & (matchFound != 1):
                    pickEntree_df = companies_df[(companies_df['Majors'].str.contains(major)) & companies_df['Entree'].between(1,7)]
                    if not pickEntree_df.empty:
                        entree_co_labels = pickEntree_df.axes[0].tolist()
                        entree_company = entree_co_labels[0]
                        matchFoundUpdate(entree_company, preference)
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
    results_df.to_excel(writer, sheet_name='All Results')
    assignments_df.to_excel(writer, sheet_name = 'Successful Assignments')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    import Analysis
    Analysis.analyze_preferences(preference_dessert_dict, preference_entree_dict)
    Analysis.analyze_major_dist(assignments_df, results_df)
