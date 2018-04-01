#!/usr/bin/python
import trello_service
import slack_service
import gsheets_service
from datetime import date, timedelta
# from oauth2client.service_account import ServiceAccountCredentials
# import smtplib
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText

def get_planned_tasks():
	with open('planned_tasks.txt', 'r') as f:
		read_data = f.read()
		return read_data

def close_sprint():
	origen = trello_service.my_board('Origen')
	done = trello_service.my_list(origen, 'Done')
	labels, members, task_count, tasks = trello_service.get_list_info(done)
	sprint_close_date = date.today()
	sprint_start_date = sprint_close_date - timedelta(days=7)
	sprint_name = "%s / %s" % (sprint_start_date, sprint_close_date)
	planned_tasks = get_planned_tasks()
	percentage = str(float(task_count) / float(planned_tasks) * 100) + ' %'
	trello_service.prepare_next_sprint(sprint_name, origen)
	slack_channel = "#origen"
	slack_message = """:loudspeaker: *Atencion:*\n
	Queridos Originarios! Es _Benito_ otra vez.\n
	Esta vez quiero darles algunos datos del sprint pasado:\n
	completaron %s de %s tareas, lo que representa un %s del sprint.\n
	Estuvo bien, pero puede ser mejor, por ahora no me comere sus zapatos.\n
	_Happy Planning_ :dog:""" % (task_count, planned_tasks, percentage )
	slack_service.send_slack_message(slack_message, slack_channel)
	gsheets_service.record_on_gsheets(sprint_name, task_count, 'close')

close_sprint()
