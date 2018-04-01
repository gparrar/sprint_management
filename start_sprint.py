#!/usr/bin/python
import trello_service
import slack_service
from datetime import date, timedelta
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import smtplib
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText

def write_planned_tasks(number):
	with open('planned_tasks.txt', 'w') as f:
		f.write(number)

def start_sprint():
    origen = trello_service.my_board('Test')
    sprint = trello_service.my_list(origen, 'To Do')
    labels, members, task_count, tasks  = trello_service.get_list_info(sprint)
    sprint_start_date = date.today()
    sprint_close_date = sprint_start_date + timedelta(days=7)
    sprint_lenght = "%s / %s" % (sprint_start_date, sprint_close_date)
    slack_channel = "#origen"
    slack_message = """:loudspeaker: *Atencion:*\n
    Queridos Originarios! Soy _Benito_ y estoy aquí para ayudarles con las tareas de este sprint.\n
    Esta semana que comienza hoy *%s* y termina el *%s* se comprometieron a terminar *%d* tareas, son las siguientes:\n
    - """  % (sprint_start_date.strftime('%m/%d/%Y'), sprint_close_date, task_count) + """\n
    - """.join(tasks) + """\n
    Si no las completan me encargaré de comerme sus objetos mas preciados.\n
    _Happy Sprint!_ :dog:"""
    write_planned_tasks(str(task_count))
    slack_service.send_slack_message(slack_message, slack_channel)

start_sprint()
