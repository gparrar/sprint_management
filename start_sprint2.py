#!/usr/bin/python

from datetime import date, timedelta
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import smtplib
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText

def find_next_avaliable_cell(col):
    values = wks.col_values(col)
    for value in values:
        if value == '':
        	index = values.index(value)
        	break
    return index + 1

def record_on_gsheets(sprint, tasks, members, labels):
        row_sprint = find_next_avaliable_cell(1)
        row_planned_tasks = find_next_avaliable_cell(2)
        bernies_tasks = wks.acell('G2').value
        gonz_tasks = wks.acell('G3').value
        lermits_tasks = wks.acell('G4').value
        nucleos_tasks = wks.acell('G6').value
        it_tasks = wks.acell('G7').value
        print type(bernies_tasks), type(members['Christian Bronstein'])
        wks.update_cell(2, 7, int(bernies_tasks) + members['Christian Bronstein'])
        wks.update_cell(3, 7, int(gonz_tasks) + members['Gonzalo Parra'])
        wks.update_cell(4, 7, int(lermits_tasks) + members['Lermit Rosell'])

        wks.update_cell(6, 7, int(nucleos_tasks) + labels['Nucleo'])
        wks.update_cell(7, 7, int(it_tasks) + labels['IT'])

        wks.update_cell(row_sprint, 1, sprint)
        wks.update_cell(row_sprint, 2, tasks)


def send_email():
	fromaddr = "originideasbar@gmail.com"
	toaddr = "gparrar@gmail.com, lermit.rg@gmail.com, chrischacal14@gmail.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Origen - Sprint del %s al %s" % (sprint_start_date, sprint_close_date)

	body = message
	msg.attach(MIMEText(body, 'html'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "J2XqAXoVaeGnO0!d")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

origin = client.get_board(get_board_id('Origin'))
sprint = origin.get_list(get_list_id(origin, 'To Do'))
sprint.fetch()
sprint_tasks = sprint.list_cards()
labels, members, task_count, tasks  = get_sprint_info()
sprint_start_date = date.today()
sprint_close_date = sprint_start_date + timedelta(days=7)
sprint_lenght = "%s / %s" % (sprint_start_date, sprint_close_date)
message = """\
<html>
	<head></head>
		<body><p><b>Atencion:</b><br><br>
				Queridos Originarios! Soy <i>Benito</i> y estoy aqui para ayudarles con las tareas de este sprint.<br><br>
				Esta semana que comienza hoy <b>%s</b> y termina el <b>%s</b> se comprometieron a terminar <b>%d</b> tareas, son las siguientes:<br>- """  % (sprint_start_date.strftime('%m/%d/%Y'), sprint_close_date, task_count) + """<br>- """.join(tasks) + """<br><br>
				Si no las completan me encargare de comerme sus objetos mas preciados.<br> <i>Happy Sprint!</i></p>
		</body>
</html>"""
#Send Slack Message
sc.api_call(
  "chat.postMessage",
  channel="#sprint",
  text=":loudspeaker: <p>Atencion:<p> \nQueridos Originarios! Soy _Benito_ y estoy aqui para ayudarles con las tareas de este sprint.\nEsta semana que comienza hoy *%s* y termina el *%s* se comprometieron a terminar *%d* tareas, son las siguientes: \n- "  % (sprint_start_date.strftime('%m/%d/%Y'), sprint_close_date, task_count) + "\n- ".join(tasks) + "\nSi no las completan me encargare de comerme sus objetos mas preciados.\n _Happy Sprint!_ :dog:"
)

# # Record on Google Sheets
record_on_gsheets(sprint_lenght,task_count, members, labels)
# # Send Emails
# send_email()
