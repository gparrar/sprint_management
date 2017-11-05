#!/usr/bin/python

from trello import TrelloClient
from collections import Counter
from slackclient import SlackClient
from datetime import date, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret2.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
try:
    wks = client.open_by_url('https://docs.google.com/spreadsheets/d/1bvZwG4J2_F1977kGKQ8xpRIsky0DXm5iJZwlfy1qYx4/edit#gid=0').worksheet('Sprint')
except (ValueError, NameError):
    print "Invalid URL"
 


slack_token = 'xoxp-245385053858-244739387712-263087848417-a00879edad580a942fd6d21752ff7e5b'
sc = SlackClient(slack_token)


client = TrelloClient(
    api_key='01d3f30b9fc6a6027e4ff6aebc5e1e51',
    api_secret='10e77f89144a7fac3d6c08458d62ab2eb73dd398d8dc1a745a43f9b6218c3925',
    token='a6d76d00692bae27f064c8142d6789c7fdccdbe94a2847e559b50665f37cddaa',
    token_secret='0211b712c27726253211e5fd108e46e7'
)

def get_board_id(my_board):	
	for board in client.list_boards():
		if my_board == board.name:
			return board.id

def get_list_id(board, my_list):
	for lista in board.list_lists():
		if lista.name == my_list:
			return lista.id

def member_name(member_id):
	return client.get_member(member_id).fetch().full_name

def get_sprint_info():
	tasks = []
	labels =  []
	members =  []
	for task in sprint_tasks:
		tasks.append(task.name)
		for label in task.labels:
			labels.append(label.name)
		for member in task.member_id:
			members.append(member_name(member))
	return Counter(labels), Counter(members), len(sprint_tasks), tasks

def prepare_next_sprint():
	name = 'Done %s' % (sprint_lenght)
	origin.add_list(name, pos='bottom')
	new_list = origin.get_list(get_list_id(origin, name))
	sprint.move_all_cards(new_list)

#este método lo puedes omitir...
#podrías cambiar:
#row_completed_tasks = find_next_available_cell(3) 
#por:
#row_completed_tasks = wks.col_values(3).index('') + 1 
def find_next_available_cell(wks, col):
    values = wks.col_values(col)
    return values.index('') + 1

def record_on_gsheets(sprint, tasks, members, labels):
        row_completed_tasks = find_next_available_cell(3) 
        bernies_tasks = wks.acell('G2').value
        gonz_tasks = wks.acell('G3').value
        lermits_tasks = wks.acell('G4').value
        nucleos_tasks = wks.acell('G6').value
        it_tasks = wks.acell('G7').value
        planned_tasks = wks.acell('B%s' % (row_completed_tasks)).value
        wks.update_cell(2, 7, int(bernies_tasks) + members['Christian Bronstein'])
        wks.update_cell(3, 7, int(gonz_tasks) + members['Gonzalo Parra'])
        wks.update_cell(4, 7, int(lermits_tasks) + members['Lermit Rosell'])
        
        wks.update_cell(6, 7, int(nucleos_tasks) + labels['Nucleo'])
        wks.update_cell(7, 7, int(it_tasks) + labels['IT'])
        
        wks.update_cell(row_completed_tasks, 3, tasks)
        percentage = wks.acell('D%s' % (row_completed_tasks)).value
        return percentage, planned_tasks

origin = client.get_board(get_board_id('Origin'))
sprint = origin.get_list(get_list_id(origin, 'Done'))
sprint.fetch()
sprint_tasks = sprint.list_cards()
labels, members, task_count, tasks  = get_sprint_info()
sprint_start_date = date.today()
sprint_close_date = sprint_start_date + timedelta(days=7)
sprint_lenght = "%s / %s" % (sprint_start_date, sprint_close_date)
percentage, planned_tasks = record_on_gsheets(sprint, tasks, members, labels)
#Send Slack Message
sc.api_call(
  "chat.postMessage",
  channel="#sprint",
  text=":loudspeaker: *Atencion:* \nQueridos Originarios! Es _Benito_ otra vez.\nEsta vez quiero darles algunos datos del sprint pasado:\n completaron *%s* de *%s* tareas, lo que representa un *%s* del sprint.\n Estuvo bien, pero ser mejor, por ahora no me comere sus zapatos.\n_Happy Planning_ :dog:" % (task_count, planned_tasks, percentage )
)

# Rename lists
prepare_next_sprint()