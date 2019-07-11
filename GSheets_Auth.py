import gspread
from oauth2client.service_account import ServiceAccountCredentials

def googleAuth():
    # Connecting to the sheet
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(credentials)
    return client
def open_user_sheets(student_file):
    client = googleAuth()
    # Get first sheet - info on students
    students = client.open(student_file).sheet1
    # Get second sheet - info on companies
    companies = client.open(student_file).get_worksheet(1)
    return students, companies
