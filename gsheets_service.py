import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
try:
    wks = client.open_by_url('https://docs.google.com/spreadsheets/d/1bvZwG4J2_F1977kGKQ8xpRIsky0DXm5iJZwlfy1qYx4/edit#gid=0').worksheet('Sprint')
except (ValueError, NameError):
    print "Invalid URL"

def find_next_avaliable_cell(col):
    values = wks.col_values(col)
    for value in values:
        if value == '':
        	index = values.index(value)
        	break
    return index + 1

def record_on_gsheets(sprint, tasks, type):
    if type == 'start':
        row_sprint = find_next_avaliable_cell(1)
        row_tasks = find_next_avaliable_cell(2)
        wks.update_cell(row_sprint, 1, sprint)
        wks.update_cell(row_tasks, 2, tasks)
    elif type == 'close':
        row_tasks = find_next_avaliable_cell(3)
        wks.update_cell(row_tasks, 3, tasks)
