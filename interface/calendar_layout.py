def doCalendar(calendarFrame):
	from Tkinter import *
	
	
	# Clear and replace calendarFrame
	for widget in calendarFrame.winfo_children():
		widget.destroy()
	
	label_8 = Label(calendarFrame, text = " 8:00 AM")
	label_9 = Label(calendarFrame, text=" 9:00 AM")
	label_10 = Label(calendarFrame, text="10:00 AM")
	label_11 = Label(calendarFrame, text="11:00 AM")
	label_12 = Label(calendarFrame, text="12:00 PM")
	label_1 = Label(calendarFrame, text=" 1:00 PM")
	label_2 = Label(calendarFrame, text=" 2:00 PM")
	label_3 = Label(calendarFrame, text=" 3:00 PM")
	label_4 = Label(calendarFrame, text=" 4:00 PM")
	label_5 = Label(calendarFrame, text=" 5:00 PM")
	label_6 = Label(calendarFrame, text=" 6:00 PM")
	label_7 = Label(calendarFrame, text=" 7:00 PM")
	label_8P = Label(calendarFrame, text=" 8:00 PM")
	label_9P = Label(calendarFrame, text=" 9:00 PM")
	label_10P = Label(calendarFrame, text="10:00 PM")
	
	label_time = Label(calendarFrame, text = "Time")
	label_M = Label(calendarFrame, text = "Monday")
	label_T = Label(calendarFrame, text = "Tuesday")
	label_W = Label(calendarFrame, text = "Wednesday")
	label_R = Label(calendarFrame, text = "Thursday")
	label_F = Label(calendarFrame, text = "Friday")
	label_S = Label(calendarFrame, text = "Saturday")
	label_Su = Label(calendarFrame, text = "Sunday")
	
	label_8.grid(row = 1, column = 0, sticky='nsew')
	label_9.grid(row = 61, column = 0, sticky='nsew')
	label_10.grid(row = 121, column = 0, sticky='nsew')
	label_11.grid(row = 181, column = 0, sticky='nsew')
	label_12.grid(row = 241, column = 0, sticky='nsew')
	label_1.grid(row = 301, column = 0, sticky='nsew')
	label_2.grid(row = 361, column = 0, sticky='nsew')
	label_3.grid(row = 421, column = 0, sticky='nsew')
	label_4.grid(row = 481, column = 0, sticky='nsew')
	label_5.grid(row = 541, column = 0, sticky='nsew')
	label_6.grid(row = 601, column = 0, sticky='nsew')
	label_7.grid(row = 661, column = 0, sticky='nsew')
	label_8P.grid(row = 721, column = 0, sticky='nsew')
	label_9P.grid(row = 781, column = 0, sticky='nsew')
	label_10P.grid(row = 841, column = 0, sticky='nsew')
	
	label_time.grid(row = 0, column = 0, sticky='nsew')
	label_M.grid(row = 0, column = 1, sticky='nsew')
	label_T.grid(row = 0, column = 2, sticky='nsew')
	label_W.grid(row = 0, column = 3, sticky='nsew')
	label_R.grid(row = 0, column = 4, sticky='nsew')
	label_F.grid(row = 0, column = 5, sticky='nsew')
	label_S.grid(row = 0, column = 6, sticky='nsew')
	label_Su.grid(row = 0, column = 7, sticky='nsew')
	
	
	for i in range(901):
		calendarFrame.rowconfigure(i, weight = 1)
	for i in range(8):
		calendarFrame.columnconfigure(i, weight = 1)
	

def get_col(day):
	days = {"M":1, "T":2, "W":3, "R":4, "F":5, "S":6, "Su":7}
	col = days[day]
	return(col)
def get_row(time):
	if time.find("A") == -1:
		add = 12
	if time.find("P") == -1:
		add = 0
	time = time.split(":")
	hour = time[0]
	# check for 12PM
	if hour == "12":
		add = 0
	min = time[1][0:1]
	hour = int(hour) + add
	hour = hour * 60
	hour = hour - (8 * 60)
	min = int(min)
	row = hour + min + 1
	return(row)
	

def block_in_Calendar(text, open, day, start, end, calendarFrame):
	from Tkinter import Label as Label
	col = get_col(day)
	row1 = get_row(start)
	row2 = get_row(end)
	span = row2 - row1
	
	if open == 1: #scheduled
		bg = "green"
	else:
		bg = "red"
	
	label = Label(calendarFrame, bg = bg, text = text, )
	label.grid(row = row1, column = col, rowspan = span, sticky='nsew')


