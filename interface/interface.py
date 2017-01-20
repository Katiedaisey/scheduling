from calendar_layout import *
#from update import *
from Tkinter import *
import sqlite3
import matrices
import numpy as np
import auto
import export
import random
import datetime as datetime
import urllib2
from bs4 import BeautifulSoup
import csv
import sys
import globalvars



# Menu and Frame Functions
def doNothing():
	print "Ok!"


def doQuit():
	root.destroy()



def doDownloadClasses():
	print 'Classes Downloaded'
	import update_classes
	#import sys
	
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='Enter 4 digit Code of Term:')
			self.myLabel.pack()
			self.myEntryBox = Entry(top)
			self.myEntryBox.pack()
			self.myLabel2 = Label(top, text='Enter Location to Save Classes: Documents/')
			self.myLabel2.pack()
			self.myEntryBox2 = Entry(top)
			self.myEntryBox2.pack()
			self.mySubmitButton = Button(top, text='Update', command=lambda: self.send())
			self.mySubmitButton.pack()
			
		def send(self):
			self.value = [self.myEntryBox.get(), self.myEntryBox2.get()]
			self.top.destroy()
		
	def onClick():
		inputDialog = MyDialog(root)
		root.wait_window(inputDialog.top)
		return(inputDialog.value)
	
	a = onClick()
	import os
	docu_path = os.path.join(os.path.expanduser("~"), "Documents")
	docu_path = docu_path + "/" + a[1]
	update_classes.update_classes(a[0], docu_path,d)
	update_classes.deleteExtraRecords(docu_path, d)
	
	message = "Classes for Term " + a[0] + " Downloaded!"
	d.set(message)
	
	


def doUpdateClasses():
	print 'Classes updated'
	import update_classes_table as uct
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel2 = Label(top, text='Enter Location of File: Documents/')
			self.myLabel2.pack()
			self.myEntryBox2 = Entry(top)
			self.myEntryBox2.pack()
			self.mySubmitButton = Button(top, text='Update', command=lambda: self.send())
			self.mySubmitButton.pack()
			
		def send(self):
			self.value = [self.myEntryBox2.get()]
			self.top.destroy()
		
	def onClick():
		inputDialog = MyDialog(root)
		root.wait_window(inputDialog.top)
		return(inputDialog.value)
	
	filename = onClick()
	docu_path = os.path.join(os.path.expanduser("~"), "Documents")
	docu_path = docu_path + "/" + filename[0]
	uct.update_classes_table(docu_path)
	message = "Analyzing Sections... Please be patient"
	d.set(message)
	global matrix_sections
	matrix_sections = matrices.matrix_sections()
	message = "Classes Updated From File"
	d.set(message)
	


def doUpdateClassWorth():
	print 'class worths updated'
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	cur.execute('SELECT ShortName, Worth From Classes')
	classes = cur.fetchall()
	
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			
			height = len(classes)
			width = 2
			for i in range(height): #Rows
				a = Label(top, text = classes[i][0])
				a.grid(row = i+1, column = 1)
				b = Entry(top)
				b.insert(END, classes[i][1])
				b.grid(row=i+1, column=2)
			
			myLabel = Label(top, text = "Update Class Worth")
			myLabel.grid(row = 0, column = 1, columnspan = 2)
			mySubmitButton = Button(top, text='Update', command=lambda: self.send())
			mySubmitButton.grid(row = 50, column = 1, columnspan = 2)
			
			
		def send(self):
			def find_in_grid(frame, row, column):
				for children in frame.children.values():
					info = children.grid_info()
					#note that rows and column numbers are stored as string                                                                         
					if info['row'] == str(row) and info['column'] == str(column):
						return children
				return None
			
			info = []
			for i in range(len(classes)):
					info.append(find_in_grid(self.top,i+1, 2).get())
			self.value = info
			self.top.destroy()
		
		
		
	def onClick():
		inputDialog = MyDialog(root)
		root.wait_window(inputDialog.top)
		return(inputDialog.value)
	
	worths = onClick()
	# update in database
	count = 0
	for cl in classes:
		cur.execute('UPDATE Classes SET Worth = ? WHERE ShortName = ?', (float(worths[count]), cl[0]))
		count = count + 1
	
	
	conn.commit()
	message = "Updated Class Worths!"
	d.set(message)
	



def doUpdateStudents():
	print 'students updated'
	import update_students_table as ust
	import matrices
	import os
	import errno
	
	def make_sure_path_exists(path):
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise
	
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='Remember to rename survey response to \'students.tsv\'!')
			self.myLabel.pack()
			self.myLabel2 = Label(top, text='Enter File To Open:')
			self.myLabel2.pack()
			self.myEntryBox2 = Entry(top)
			self.myEntryBox2.pack()
			self.mySubmitButton = Button(top, text='Update', command=self.send)
			self.mySubmitButton.pack()
			
		def send(self):
			self.value = self.myEntryBox2.get()
			self.top.destroy()
		
	def onClick():
		inputDialog = MyDialog(root)
		root.wait_window(inputDialog.top)
		return(inputDialog.value)
		
	
	filename = onClick()
	docu_path = os.path.join(os.path.expanduser("~"), "Documents")
	docu_path = docu_path + "/" + filename
	ust.update_students_table(docu_path, d)
	matrices.matrix_pref(d)
	globalvars.mat_prefs = np.load(globalvars.mat_prefs_path)
	
	message = "Student Responses Updated!"
	d.set(message)
	



# List Classes in popup box for google forms survey
def doListClasses():
	print 'doListClasses'
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	
	classes = cur.execute('SELECT ShortName, Name FROM Classes')
	classes = cur.fetchall()
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='List of Classes:')
			self.myLabel.pack()
			self.myframe = Frame(top)
			self.myframe.pack(fill = BOTH)
			T = Text(self.myframe)
			T.pack()
			def addtolist(item):
				T.insert(END, item[0] + " - " + item[1] + "\n")
			for item in classes:
				addtolist(item = item)	
			self.mySubmitButton = Button(top, text='Finished', command=self.send)
			self.mySubmitButton.pack()
			
			
			
			
		def send(self):
			self.top.destroy()
		
	def onClick():
	    inputDialog = MyDialog(root)
	    root.wait_window(inputDialog.top)
	    return()
	
	onClick()
	




def doListProfessors():
	print 'doListProfessors'
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	
	profs = cur.execute('SELECT Name FROM Professors')
	profs = cur.fetchall()
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='List of Professors:')
			self.myLabel.pack()
			self.myframe = Frame(top)
			self.myframe.pack(fill = BOTH)
			T = Text(self.myframe)
			T.pack()
			def addtolist(item):
				T.insert(END, str(item[0])[1:-1] + "\n")
			for item in profs:
				addtolist(item = item)	
			self.mySubmitButton = Button(top, text='Finished', command=self.send)
			self.mySubmitButton.pack()
			
			
			
		def send(self):
			self.top.destroy()
		
	def onClick():
	    inputDialog = MyDialog(root)
	    root.wait_window(inputDialog.top)
	    return()
	
	onClick()
	


class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, text = "Welcome!", bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()



def doByClass():
	print 'doByClass'
	global scheduling
	scheduling = 'class'
	
	leftListbox.delete(0,END)
	chosenListbox.delete(0,END)
	openListbox.delete(0,END)
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	
	classes = cur.execute('SELECT ShortName, Name FROM Classes')
	classes = cur.fetchall()
	
	for item in classes:
		leftListbox.insert(END, item)
	

def doByStudent():
	print 'doByStudent'
	global scheduling
	scheduling = 'student'
	leftListbox.delete(0,END)
	chosenListbox.delete(0,END)
	openListbox.delete(0,END)
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	
	classes = cur.execute('SELECT StudentID, Name, Scheduled FROM Students')
	classes = cur.fetchall()
	
	
	for item in classes:
		item = str(item[0]) + ": " + item[1] + " (" + str(item[2]) + ")"
		leftListbox.insert(END, item)
	

def doAutomateFast():
	print 'AutomateFast'
	doSave(output2 = output)
	message = "Generating TA Lines"
	d.set(message)
	auto.gen_sec_matrix(pop = 100, keep = 10, output = output)
	auto.break_up(output)
	global mat_sch
	message = "Matching TAs with Lines"
	d.set(message)
	mat_sch = auto.gen_sec_stu_matrix(pop = 1000, keep = 1, mats = 10, output = output)[0]
	
	
	global output
	auto.updateDatabase(mat_sch, output)
	message = "Schedule Created!"
	d.set(message)
	
	return()

def doAutomateBest():
	print 'doAutomateBest'
	doSave(output2 = output)
	message = "Generating TA Lines"
	d.set(message)
	auto.gen_sec_matrix(pop = 1000, keep = 100, output = output)
	auto.break_up(output)
	global mat_sch
	global mat_prefs
	message = "Matching TAs with Lines"
	d.set(message)
	mat_sch = auto.gen_sec_stu_matrix(pop = 10000, keep = 1, mats = 100, output = output)[0]
	auto.updateDatabase(mat_sch, output)
	message = "Schedule Created!"
	d.set(message)
	return()
	
	


def doViewClass():
	print 'doViewClass'
	current = leftListbox.get(ANCHOR)[0]
	global current_class
	current_class = current
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	
	classes = cur.execute('''
		SELECT B.SectionID, B.Scheduled, B.Name, D.Day, D.Start, D.End
		FROM Classes A INNER JOIN Sections B
		ON A.ClassID = B.ClassID
		INNER JOIN Sections_Times C
		ON B.SectionID = C.SectionID
		INNER JOIN Times D
		ON C.TimeID = D.TimeID
		WHERE A.ShortName = ?''', (current,))
	classes = cur.fetchall()
	cur.execute('''
		SELECT B.StudentID, B.Name, A.SectionID
		FROM Sections A INNER JOIN Students B
		ON A.StudentID = B.StudentID
		INNER JOIN Classes C
		ON A.ClassID = C.ClassID
		WHERE C.ShortName = ?''', (current,))
	tas = cur.fetchall()
	lines = dict()
	for ta in tas:
		lines[ta[2]] = ta[1]
	doCalendar(calendarFrame)
	info = []
	multiclass = dict()
	for cl in classes:
		name = "0"
		if cl[1] == 1:
			name = lines[cl[0]]
		if len(cl[3]) > 1:
			for c in cl[3]:
				try:
					
					block_in_Calendar(text = cl[2] + " (" + name + ")", open = cl[1], day =  c, start = cl[4], end = cl[5], calendarFrame = calendarFrame)
				except:
					info.append(cl[2] + ": " + name + " " + cl[4] + "-" + cl[5])
		else:
			try:
				
				block_in_Calendar(text = cl[2] + " (" + name + ")", open =  cl[1], day =  cl[3], start = cl[4], end = cl[5], calendarFrame = calendarFrame)
			except:
				continue
				#info.append(cl[2] + ": " + name + " " + cl[4] + "-" + cl[5])
	
	
	add_info_Calendar(text = info, calendarFrame = calendarFrame)
	return()

def doViewStudent(student):
	print 'doViewStudent'
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	# immediate time conflicts
	unavail = cur.execute('''SELECT D.Day, D.Start, D.End
		FROM Con_Student_Time B INNER JOIN Times D
		ON B.TimeID = D.TimeID
		WHERE B.StudentID = ?''', (student, ))
	unavail = cur.fetchall()
	for ut in unavail:
		block_in_Calendar(text = '', open = 3, day = ut[0], start = ut[1], end = ut[2], calendarFrame = calendarFrame)
	
	prefer = cur.execute('''SELECT D.Day, D.Start, D.End
		FROM Pref_Student_Time B INNER JOIN Times D
		ON B.TimeID = D.TimeID
		WHERE B.StudentID = ?''', (student, ))
	prefer = cur.fetchall()
	for pt in prefer:
		block_in_Calendar(text = '', open = 2, day = pt[0], start = pt[1], end = pt[2], calendarFrame = calendarFrame)
	cur.execute('SELECT Year, Division, Skill FROM Students WHERE StudentID = ?', (student,))
	info = cur.fetchone()
	add_info_Calendar(text = "Year: " + str(info[0]) + ", Div: " + str(info[1]) + ', Skill: ' + str(info[2]), calendarFrame = calendarFrame)
	
	
	
	sch = cur.execute('SELECT Scheduled From Students WHERE StudentID = ?', (student,))
	sch = cur.fetchone()
	if sch[0] > 0:
		sch_classes = cur.execute('''SELECT A.Name, C.ShortName, B.Name, D.Day, D.Start, D.End
			FROM Students A INNER JOIN Sections B
			ON A.StudentID = B.StudentID
			INNER JOIN Classes C
			ON B.ClassID = C.ClassID
			INNER JOIN Sections_Times E
			ON B.SectionID = E.SectionID
			INNER JOIN Times D
			ON E.TimeID = D.TimeID
			WHERE A.StudentID = ?''', (student,))
		sch_classes = cur.fetchall()
		for cl in sch_classes:
			if len(cl[3]) > 1:
				for c in cl[3]:
					try:
						block_in_Calendar(text = cl[1] + " " + cl[2], open = 1, day = c, start = cl[4], end = cl[5], calendarFrame = calendarFrame)
					except:
						continue
			else:
				try:
					block_in_Calendar(text = cl[1] + " " + cl[2], open = 1, day = cl[3], start = cl[4], end = cl[5], calendarFrame = calendarFrame)
				except:
					continue
			
		


def leftselect(): #Select
	if scheduling == 'class':
		print 'leftselect-class'
		doViewClass()
		current = leftListbox.get(ANCHOR)[0]
		global current_class
		current_class = current
		chosenListbox.delete(0, END)
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		
		classes = cur.execute('''
			SELECT B.Scheduled, B.Name, D.Day, D.Time
			FROM Classes A INNER JOIN Sections B
			ON A.ClassID = B.ClassID
			INNER JOIN Sections_Times C
			ON B.SectionID = C.SectionID
			INNER JOIN Times D
			ON C.TimeID = D.TimeID
			WHERE A.ShortName = ?''', (current_class,))
		classes = cur.fetchall()
		
		# Insert sections in middle box
		chosenListbox.insert(END, "any")
		for item in classes:
			#if item[0] != 0:
			#	item[0] = 1
			chosenListbox.insert(END, item)
	
	
	if scheduling == 'student':
		print 'leftselect-student'
		doCalendar(calendarFrame)
		current = leftListbox.get(ANCHOR)
		global current_student
		current_student = current
		stu = current.split(":")[0]
		chosenListbox.delete(0, END)
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		
		cur.execute('''SELECT B.SectionID, C.ShortName, B.Name
			FROM Students A INNER JOIN Sections B
			ON A.StudentID = B.StudentID
			INNER JOIN Classes C
			ON B.ClassID = C.ClassID
			WHERE A.StudentID = ?''', (stu,))
		classes = cur.fetchall()
		
		doViewStudent(stu)
		
		# Insert assigned sections in middle box
		#chosenListbox.insert(END, "any")
		for item in classes:
			item = item[1] + " " + item[2]
			chosenListbox.insert(END, item)
		
		# Insert classes in right box
		# centerselect will select class to view sections
		openListbox.delete(0,END)
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
	
		classes = cur.execute('SELECT ShortName, Name FROM Classes')
		classes = cur.fetchall()
	
		for item in classes:
			openListbox.insert(END, item)





# get students available for current section
# list in order of mat_prefs value
def centerselect(): #View
	if scheduling == 'class':
		print 'centerselect-class'
		current = chosenListbox.get(ANCHOR)
		global current_section
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		if current == "any":
			current_section = "any"
		else:
			current_section = current[1]
			
			
			cla = cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?',(current_class,))
			cla = cur.fetchone()[0]
			sec1 = cur.execute('SELECT SectionID FROM Sections WHERE ClassID = ? and Name = ?', (cla, current_section))
			global sec
			sec = cur.fetchone()[0]
		
		
		students = cur.execute('SELECT DISTINCT Name, StudentID, Scheduled FROM Students WHERE Scheduled < 0.9') # ie less than fully scheduled
		students = cur.fetchall()
		global mat_prefs
		student_tuples = []
		for i in range(len(students)):
			if  current_section != "any":
				colnum = section_index[sec]
				stu = students[i][1]
				stuID = student_index[stu]
				student_tuples.append((int(globalvars.mat_prefs[stuID,colnum]),(students[i][1],students[i][0], students[i][2]),i)) # update from i to stuindex
			else:
				student_tuples.append((int(0),(students[i][1], students[i][0], students[i][2]),i))
		# sort p in order of highest value first
		openListbox.delete(0,END)
		if current_section != "any":
			student_tuples = sorted(student_tuples, key = lambda student:student[0], reverse = True)
		for item in student_tuples:
			item = str(item[0]) + "; " + str(item[1][1]) + " (" + str(item[1][2]) + ")" 
			openListbox.insert(END, item)
		openListbox.insert(END, "undergrad")
		
		
		students = cur.execute('SELECT DISTINCT Name, StudentID, Scheduled FROM Students WHERE Scheduled > 0.9') # ie fully scheduled
		students = cur.fetchall()
		global mat_prefs
		student_tuples = []
		for i in range(len(students)):
			if  current_section != "any":
				colnum = section_index[sec]
				stu = students[i][1]
				stuID = student_index[stu]
				student_tuples.append((int(globalvars.mat_prefs[stuID,colnum]),(students[i][1],students[i][0], students[i][2]),i)) # update from i to stuindex
			else:
				student_tuples.append((int(0),(students[i][1], students[i][0], students[i][2]),i))
		# sort p in order of highest value first
		if current_section != "any":
			student_tuples = sorted(student_tuples, key = lambda student:student[0], reverse = True)
		for item in student_tuples:
			item = str(item[0]) + "; " + str(item[1][1]) + " (" + str(item[1][2]) + ")" 
			openListbox.insert(END, item)
		
	
	if scheduling == 'student':
		print 'centerselect-student'
		current = openListbox.get(ANCHOR)[0]
		global current_class
		current_class = current
		openListbox.delete(0, END)
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		
		classes = cur.execute('''
			SELECT B.Scheduled, B.Name, D.Day, D.Time
			FROM Classes A INNER JOIN Sections B
			ON A.ClassID = B.ClassID
			INNER JOIN Sections_Times C
			ON B.SectionID = C.SectionID
			INNER JOIN Times D
			ON C.TimeID = D.TimeID
			WHERE A.ShortName = ?''', (current_class,))
		classes = cur.fetchall()
		
		# Insert sections in middle box
		openListbox.insert(END, "any")
		for item in classes:
			#if item[0] != 0:
			#	item[0] = 1
			openListbox.insert(END, item)



def get_class_value(SectionID):
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	cla = cur.execute('''SELECT A.Worth from Classes A Inner Join Sections B ON A.ClassID = B.ClassID WHERE B.SectionID = ?''', (SectionID,))
	cla = cur.fetchone()[0]
	return(cla)


def openaddselect(): #Schedule
	# schedule student to class
	if scheduling == 'class':
		print 'add-class'
		current = openListbox.get(ANCHOR)
		current = current.split("; ")[1]
		current = current.split(" (")[0]
		
		
		
		
		sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		stu = cur.execute('SELECT StudentID FROM Students WHERE Name = ?',(current[0],))
		stu = cur.fetchone()[0]
		
		
		
		# byClass add student to specific section of class
		if current_section != "any":
			cur.execute('''SELECT A.SectionID FROM Sections A INNER JOIN 
				Classes B ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ? and A.Name = ?
				''', (current_class,current_section))
			sec = cur.fetchone()[0]
			
			global mat_yes
			global mat_no
			stuID = student_index[stu]
			secID = section_index[sec] # what's sec from
			mat_yes[stuID, secID] = 1
			mat_no[stuID, secID] = 0
			addPrefForClass(stu)
			value = get_class_value(sec)
			oldvalue = cur.execute('SELECT Scheduled FROM Students WHERE StudentID = ?',(stu, ) )
			oldvalue = cur.fetchone()[0]
			c = cur.execute('UPDATE Students SET Scheduled = ? WHERE StudentID = ?',(float(value) + float(oldvalue), stu) )
			c = cur.execute('UPDATE Sections SET Scheduled = ? WHERE SectionID = ?' , (1, sec))
			c = cur.execute('UPDATE Sections SET StudentID = ? WHERE SectionID = ?', (stu, sec)) # wonder why this doesn't work with an AND statement
			conn.commit()
		
		# byClass add student to any section of class
		if current_section == "any":
			print 'any'
			addPrefForClass(stu)
			global mat_yes
			global mat_add
			global mat_no
			cur.execute('SELECT A.SectionID FROM Sections A INNER JOIN Classes B ON A.ClassID = B.ClassID WHERE B.ShortName = ?',(current_class,))
			secs = fetchall()
			global section_index
			for sec in secs:
				secID = section_index[sec[0]]
				mat_yes[stuID,secID] = 0
				mat_add[stuID,secID] = 1
				mat_no[stuID,secID] = 0
				
			
			value = get_class_value(secs[0])
			oldvalue = cur.execute('SELECT Scheduled FROM Students WHERE StudentID = ?',(stu, ) )
			oldvalue = cur.fetchone()[0]
			c = cur.execute('UPDATE Students SET Scheduled = ? WHERE StudentID = ?',(float(oldvalue) + float(value),  stu) )
			conn.commit()
				
		
		
		doViewClass()
		message = "Student Added to Class!"
		centerselect()
		d.set(message)
	
	
	
	if scheduling == 'student':
		print 'add-student'
		current = openListbox.get(ANCHOR)
		global current_section
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		if current == "any":
			current_section = "any"
		else:
			current_section = current[1]
		
		
		stu = current_student.split(":")[0]
		stu = int(stu)
		global student_index
		stuID = student_index[stu]
		
		# byStudent add student to single section of class
		if current_section != "any":
			cur.execute('''SELECT A.SectionID FROM Sections A INNER JOIN 
				Classes B ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ? and A.Name = ?
				''', (current_class,current_section))
			sec = cur.fetchone()[0]
			
			# mats
			global mat_yes
			global mat_no
			
			
			
			secID = section_index[sec] # what's sec from
			mat_yes[stuID, secID] = 1
			mat_no[stuID, secID] = 0
			addPrefForClass(stu)
			
			# database
			value = get_class_value(sec)
			oldvalue = cur.execute('''SELECT Scheduled FROM Students 
				WHERE StudentID = ?''',(stu, ) )
			oldvalue = cur.fetchone()[0]
			c = cur.execute('''UPDATE Students SET Scheduled = ? 
				WHERE StudentID = ?''',(float(value) + float(oldvalue), stu) )
			c = cur.execute('''UPDATE Sections SET Scheduled = ? 
				WHERE SectionID = ?''' , (1, sec))
			c = cur.execute('''UPDATE Sections SET StudentID = ? 
				WHERE SectionID = ?''', (stu, sec)) 
			# wonder why this doesn't work with an AND statement
			
			
			# Insert assigned sections in middle box
			#chosenListbox.insert(END, "any")
			cur.execute('''SELECT B.SectionID, C.ShortName, B.Name
			FROM Students A INNER JOIN Sections B
			ON A.StudentID = B.StudentID
			INNER JOIN Classes C
			ON B.ClassID = C.ClassID
			WHERE A.StudentID = ?''', (stu,))
			classes = cur.fetchall()
			
			
			chosenListbox.delete(0, END)
			for item in classes:
				item = item[1] + " " + item[2]
				chosenListbox.insert(END, item)
			
			conn.commit()
		
		#byStudent add student to any section of class
		if current_section == "any":
			print 'any'
			
			# add in mats
			addPrefForClass(stu)
			global mat_yes
			global mat_add
			global mat_no
			cur.execute('''SELECT A.SectionID FROM Sections A 
				INNER JOIN Classes B 
				ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ?''',(current_class,))
			secs = cur.fetchall()
			global section_index
			for sec in secs:
				secID = section_index[sec[0]]
				mat_yes[stuID,secID] = 0
				mat_add[stuID,secID] = 1
				mat_no[stuID,secID] = 0
			
			# add in database
			value = get_class_value(secs[0][0])
			oldvalue = cur.execute('''SELECT Scheduled FROM Students 
				WHERE StudentID = ?''',(stu, ) )
			oldvalue = cur.fetchone()[0]
			c = cur.execute('''UPDATE Students SET Scheduled = ? 
				WHERE StudentID = ?''',(float(oldvalue) + float(value),  stu) )
			conn.commit()
			chosenListbox.insert(END, 'any ' + current_class)
		
		
		
		
		
		doViewStudent(stu)
		message = "Student Added to Class!"
		
		d.set(message)

def openremoveselect(): #Remove
	# remove student from class
	if scheduling == 'class':
		print 'remove-class'
		current = openListbox.get(ANCHOR)
		current = current.split("; ")[1]
		current = current.split(" (")
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		stu = cur.execute('SELECT StudentID FROM Students WHERE Name = ?',(current[0],))
		stu = cur.fetchone()[0]
		
		# byClass remove student from single section
		if current_section != "any":
			cur.execute('''SELECT A.SectionID FROM Sections A INNER JOIN 
				Classes B ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ? and A.Name = ?
				''', (current_class,current_section))
			sec = cur.fetchone()[0]
			
			
			# mats
			global mat_yes
			global student_index
			global section_index
			stuID = student_index[stu]
			secID = section_index[sec]
			mat_yes[stuID, secID] = 0
			
			# remove from database
			value = get_class_value(sec)
			oldvalue = cur.execute('SELECT Scheduled FROM Students WHERE StudentID = ?',(stu, ) )
			oldvalue = cur.fetchone()[0]
			cur.execute('''UPDATE Students SET Scheduled = ? 
				WHERE StudentID = ?''',(oldvalue - value, stu) )
			cur.execute('''Update Sections SET Scheduled = ? 
				WHERE SectionID = ?''' , (0, sec))
			cur.execute('''Update Sections SET StudentID = ? 
				WHERE SectionID = ?''' , (stu, sec))
			
			conn.commit()
		
		# byClass remove student from any section
		if current_section == "any":
			print 'any'
			
			# remove scheduled from mats
			global mat_yes
			global mat_add
			cur.execute('''SELECT A.SectionID FROM Sections A 
				INNER JOIN Classes B 
				ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ?''',(current_class,))
			secs = cur.fetchall()
			global section_index
			for sec in secs:
				secID = section_index[sec[0]]
				mat_yes[stuID,secID] = 0
				mat_add[stuID,secID] = 0
			
			# remove scheduled from database
			value = get_class_value(secs[0][0])
			oldvalue = cur.execute('''SELECT Scheduled FROM Students 
				WHERE StudentID = ?''',(stu, ) )
			oldvalue = cur.fetchone()[0]
			c = cur.execute('''Update Students SET Scheduled = ? 
				WHERE StudentID = ?''',(float(oldvalue) - float(value), stu) )
			conn.commit()
		
		doViewClass()
		message = "Student Removed from Class!"
		d.set(message)
	
	
	
	if scheduling == 'student':
		print 'remove-student'
		current = openListbox.get(ANCHOR)
		global current_section
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		if current == "any":
			current_section = "any"
		else:
			current_section = current[1]
		
		stu = current_student.split(":")[0]
		stu = int(stu)
		global student_index
		stuID = student_index[stu]
		
		# byStudent remove student from single section of class
		if current_section != "any":
			cur.execute('''SELECT A.SectionID FROM Sections A INNER JOIN 
				Classes B ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ? and A.Name = ?
				''', (current_class,current_section))
			sec = cur.fetchone()[0]
			
			# mats
			global mat_yes
			global mat_no
			global section_index
			secID = section_index[sec] # what's sec from
			mat_yes[stuID, secID] = 1
			mat_no[stuID, secID] = 0
			addPrefForClass(stu)
			
			# remove from database
			value = get_class_value(sec)
			oldvalue = cur.execute('SELECT Scheduled FROM Students WHERE StudentID = ?',(stu, ) )
			oldvalue = cur.fetchone()[0]
			c = cur.execute('UPDATE Students SET Scheduled = ? WHERE StudentID = ?',(float(value) - float(oldvalue), stu) )
			c = cur.execute('UPDATE Sections SET Scheduled = ? WHERE SectionID = ?' , (0, sec))
			c = cur.execute('UPDATE Sections SET StudentID = ? WHERE SectionID = ?', (0, sec)) # wonder why this doesn't work with an AND statement
			
			
			# Insert assigned sections in middle box
			#chosenListbox.insert(END, "any")
			cur.execute('''SELECT B.SectionID, C.ShortName, B.Name
			FROM Students A INNER JOIN Sections B
			ON A.StudentID = B.StudentID
			INNER JOIN Classes C
			ON B.ClassID = C.ClassID
			WHERE A.StudentID = ?''', (stu,))
			classes = cur.fetchall()
			
			
			chosenListbox.delete(0, END)
			for item in classes:
				item = item[1] + " " + item[2]
				chosenListbox.insert(END, item)
			
			conn.commit()
		
		
		# byStudent remove from any section
		if current_section == "any":
			print 'any'
			global current_class
			removePrefForClass(stu)
			
			# mats
			global mat_yes
			global mat_add
			global mat_no
			cur.execute('SELECT A.SectionID FROM Sections A INNER JOIN Classes B ON A.ClassID = B.ClassID WHERE B.ShortName = ?',(current_class,))
			secs = cur.fetchall()
			global section_index
			for sec in secs:
				secID = section_index[sec[0]]
				mat_yes[stuID,secID] = 0
				mat_add[stuID,secID] = 1
				mat_no[stuID,secID] = 0
			
			# remove from database
			value = get_class_value(secs[0][0])
			oldvalue = cur.execute('SELECT Scheduled FROM Students WHERE StudentID = ?',(stu, ) )
			oldvalue = cur.fetchone()[0]
			c = cur.execute('UPDATE Students SET Scheduled = ? WHERE StudentID = ?',(float(oldvalue) - float(value),  stu) )
			conn.commit()
			
			items = chosenListbox.get(0,END)
			a = items.index('any ' + current_class)
			chosenListbox.delete(a)
			
			
		
		
		
		
		
		doViewStudent(stu)
		message = "Student Removed from Class!"
		d.set(message)



def openaddblockselect(): #Add Block
	# block student from class
	if scheduling == 'class':
		print 'block-class'
		current = openListbox.get(ANCHOR)
		current = current.split("; ")[1]
		current = current.split(" (")
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		stu = cur.execute('SELECT StudentID FROM Students WHERE Name = ?',(current[0],))
		stu = cur.fetchone()[0]
		global student_index
		stuID = student_index[stu]
		
		# byClass block student from single section of class
		if current_section != "any":
			cur.execute('''SELECT A.SectionID FROM Sections A INNER JOIN 
				Classes B ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ? and A.Name = ?
				''', (current_class,current_section))
			sec = cur.fetchone()[0]
			
			global mat_yes
			global mat_no
			global section_index
			secID = section_index[sec]
			mat_yes[stuID, secID] = 0
			mat_no[stuID, secID] = 1
		
		# byClass block of student from any section in class
		if current_section == 'any':
			print 'any'
			removePrefForClass(stu)
			
			cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?', (current_class,))
			ClassID = cur.fetchone()[0]
			cur.execute('SELECT SectionID FROM Sections WHERE ClassID = ?'
			, (ClassID,))
			secs = cur.fetchall()
			for sec in secs:
				secID = section_index[sec[0]]
				mat_yes[stuID,secID] = 0
				mat_no[stuID,secID] = 1
			
			
		conn.commit()
	
	
	# byStudent block from class
	if scheduling == 'student':
		print 'block-student'
		current = openListbox.get(ANCHOR)
		global current_section
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		if current == "any":
			current_section = "any"
		else:
			current_section = current[1]
		
		stu = current_student.split(":")[0]
		stu = int(stu)
		global student_index
		stuID = student_index[stu] #where stu from
		
		# byStudent block from single section of class
		if current_section != 'any':
			global mat_yes
			global mat_no
			global section_index
			cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?',(current_class,))
			cla = cur.fetchone()[0]
			cur.execute('SELECT SectionID FROM Sections WHERE ClassID = ? and Name = ?', (cla, current_section))
			sec = cur.fetchone()[0]
			secID = section_index[sec]
			mat_yes[stuID,secID] = 0
			mat_no[stuID,secID] = 1
		
		#by Student block of any section of class
		if current_section == 'any':
			print 'any'
			global mat_yes
			global mat_no
			global section_index
			cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?', (current_class,))
			cla = cur.fetchone()[0]
			cur.execute('SELECT SectionID FROM Sections WHERE ClassID = ?'
			, (cla,))
			secs = cur.fetchall()
			for sec in secs:
				secID = section_index[sec[0]]
				mat_yes[stuID,secID] = 0
				mat_no[stuID,secID] = 1
			removePrefForClass(stu)
		
	message = "Student Blocked From Class!"
	d.set(message)
	
def openremoveblockselect(): #Remove Block
	# remove block from student from class
	if scheduling == 'class':
		print 'rmblock-class'
		current = openListbox.get(ANCHOR)
		current = current.split("; ")[1]
		current = current.split(" (")
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		stu = cur.execute('SELECT StudentID FROM Students WHERE Name = ?',(current[0],))
		stu = cur.fetchone()[0]
		global student_index
		stuID = student_index[stu]
		
		# byClass remove block from single section of class
		if current_section != 'any':
			cur.execute('''SELECT A.SectionID FROM Sections A 
				INNER JOIN Classes B ON A.ClassID = B.ClassID 
				WHERE B.ShortName = ? and A.Name = ?
				''', (current_class,current_section))
			sec = cur.fetchone()
			global mat_no
			global section_index
			secID = section_index[sec]
			mat_no[stuID, secID] = 0
		
		# byClass remove block from any section of class
		if current_section == 'any':
			print 'any'
			addPrefForClass(stu)
			
			cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?', (current_class,))
			ClassID = cur.fetchone()[0]
			cur.execute('SELECT SectionID FROM Sections WHERE ClassID = ?'
			, (ClassID,))
			secs = cur.fetchall()
			for sec in secs:
				secID = section_index[sec[0]]
				mat_yes[stuID,secID] = 0
				mat_no[stuID,secID] = 0
		conn.commit()
		
	
	if scheduling == 'student':
		print 'rmblock-student'
		current = openListbox.get(ANCHOR)
		global current_section
		globalvars.database_path
		conn = sqlite3.connect(globalvars.database_path)
		cur = conn.cursor()
		if current == "any":
			current_section = "any"
			print 'any-not yet supported'
		else:
			current_section = current[1]
		
		stu = current_student.split(":")[0]
		stu = int(stu)
		global student_index
		stuID = student_index[stu]
		
		# byStudent remove block from single section of class
		if current_section != 'any':
			global mat_yes
			global mat_no
			global section_index
			cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?',(current_class,))
			cla = cur.fetchone()[0]
			cur.execute('SELECT SectionID FROM Sections WHERE ClassID = ? and Name = ?', (cla, current_section))
			sec = cur.fetchone()[0]
			secID = section_index[sec[0]]
			mat_yes[stuID,secID] = 0
			mat_no[stuID,secID] = 0
			
	
	message = "Student Block Removed!"
	d.set(message)


def addPrefForClass(student):
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	secs = cur.execute('''SELECT A.SectionID FROM Classes B
		INNER JOIN Sections A 
		ON A.ClassID = B.ClassID
		WHERE B.ShortName = ?''', (current_class,))
	secs = cur.fetchall()
	stuID = student_index[student]
	for s in secs:
		secID = section_index[s[0]]
		cpref = globalvars.mat_prefs[stuID,secID]
		globalvars.mat_prefs[stuID,secID] = int(cpref) + 10000

def removePrefForClass(student):
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	secs = cur.execute('''SELECT A.SectionID FROM Classes B
		INNER JOIN Sections A 
		ON A.ClassID = B.ClassID
		WHERE B.ShortName = ?''', (current_class,))
	secs = cur.fetchall()
	stuID = student_index[student]
	for s in secs:
		secID = section_index[s[0]]
		cpref = globalvars.mat_prefs[stuID,secID]
		globalvars.mat_prefs[stuID,secID] = int(cpref) - 10000


# File functions

def doNewSchedule():
	print 'doNewSchedule'
	import numpy as np
	import globalvars
	message = "Starting a New Schedule"
	d.set(message)
	# Data
	try:
		# open from file
		globalvars.mat_prefs = np.load(globalvars.mat_prefs_path)
	except:
		# generate if unable to open
		message = "Generating Missing Files"
		d.set(message)
		globalvars.mat_prefs = matrices.matrix_pref(d)
	global section_index
	section_index = matrices.section_index()
	global student_index
	student_index = matrices.student_index()
	global mat_yes
	mat_yes = matrices.matrix_schedule_manual()
	global mat_add
	mat_add = matrices.matrix_schedule_manual()
	global mat_no
	mat_no = matrices.matrix_schedule_manual()
	try:
		globalvars.matrix_sections = np.load(globalvars.sec_sec_matrix_path)
		
	except:
		try:
			message = "Generating Missing Files"
			d.set(message)
			globalvars.matrix_sections = matrices.matrix_sections()
		except:
			globalvars.matrix_sections = np.zeros((100,100))
	globalvars.matrix_sections.flags.writeable = True
	
	
	global output
	output = "output"
	
	global scheduling
	global mat_sch
	global current_class
	global current_student
	global current_section
	global sec
	
	
	
	
	# update database
	globalvars.database_path
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	cur.execute('UPDATE Sections SET Scheduled = 0')
	cur.execute('UPDATE Sections SET StudentID = 0')
	cur.execute('UPDATE Students SET Scheduled = 0')
	conn.commit()
	
	message = "New Schedule"
	d.set(message)



def doOpenSchedule(output2 = None):
	print 'doOpenSchedule'
	import os
	import errno
	
	def make_sure_path_exists(path):
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise

	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='Enter Name To Open:')
			self.myLabel.pack()
			self.myEntryBox = Entry(top)
			self.myEntryBox.pack()
			self.mySubmitButton = Button(top, text='Open', command=self.send)
			self.mySubmitButton.pack()
			
		def send(self):
			self.value = self.myEntryBox.get()
			self.top.destroy()
		
	def onClick():
		inputDialog = MyDialog(root)
		root.wait_window(inputDialog.top)
		return(inputDialog.value)
	
	if output2 is None:
		global output
		output = onClick()
	else:
		global output
		output = output2
	make_sure_path_exists(output)
	
	global mat_yes
	mat_yes = np.load(output + "/mat_yes.npy")
	global mat_add
	mat_add = np.load(output + "/mat_add.npy")
	global mat_no
	mat_no = np.load(output + "/mat_no.npy")
	globalvars.matrix_sections = np.load(output + "/matrix_sections.npy")
	globalvars.mat_prefs = np.load(output + "/mat_prefs.npy") # matrices.matrix_pref()
	global section_index
	section_index = matrices.section_index()
	global student_index
	student_index = matrices.student_index()
	
	message = "Openned Schedule from " + output
	d.set(message)



def doSave(output2):
	print 'doSave'
	np.save(output2 + "/mat_yes.npy", mat_yes)
	np.save(output2 + "/mat_add.npy", mat_add)
	np.save(output2 + "/mat_no.npy", mat_no)
	np.save(output2 + "/matrix_sections.npy", globalvars.matrix_sections)
	np.save(output2 + "/mat_prefs.npy", globalvars.mat_prefs)
	message = "Schedule Saved"
	d.set(message)



def doSaveAs():
	print 'doSaveAs'
	
	import os
	import errno
	
	def make_sure_path_exists(path):
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise
				
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='Enter Name To Save Output:')
			self.myLabel.pack()
			self.myEntryBox = Entry(top)
			self.myEntryBox.pack()
			self.mySubmitButton = Button(top, text='Save', command=self.send)
			self.mySubmitButton.pack()
			
		def send(self):
			self.value = self.myEntryBox.get()
			self.top.destroy()
		
	def onClick():
		inputDialog = MyDialog(root)
		root.wait_window(inputDialog.top)
		return(inputDialog.value)
	
	global output
	output = onClick()
	
	make_sure_path_exists(output)
	#np.save(output + "/automats", automats)
	np.save(output + "/mat_yes.npy",mat_yes)
	np.save(output + "/mat_add.npy", mat_add)
	np.save(output + "/mat_no.npy", mat_no)
	np.save(output + "/mat_prefs.npy", globalvars.mat_prefs)
	np.save(output + "/matrix_sections.npy", globalvars.matrix_sections)
	message = "Schedule Saved"
	d.set(message)





# Main loop
root = Tk()


# Layout Frames
navFrame = Frame(root)
statusFrame = Frame(root)
calendarFrame = Frame(root)




navFrame.pack(side = TOP)
statusFrame.pack(side = BOTTOM, fill = X)
calendarFrame.pack(side = BOTTOM, fill = BOTH)
doCalendar(calendarFrame)



d = StatusBar(statusFrame)
d.pack(side = LEFT)
leftListbox = Listbox(navFrame)
leftListbox.pack(side = LEFT)



buttonSelectFrame = Frame(navFrame)
buttonSelectFrame.pack(side = LEFT)
bselect = Button(buttonSelectFrame, text="Select", command=lambda : leftselect()) # lambda necessary to prevent call upon opening
bselect.pack(side = TOP)

chosenListbox = Listbox(navFrame)
chosenListbox.pack(side = LEFT)


buttonFrame = Frame(navFrame)
buttonFrame.pack(side = LEFT)
bAdd = Button(buttonFrame, text="View", command=lambda : centerselect())
bAdd.pack(side = TOP)


openListbox = Listbox(navFrame)
openListbox.pack(side = LEFT)
buttonFrame2 = Frame(navFrame)
buttonFrame2.pack(side = LEFT)
bRemove = Button(buttonFrame2, text="Schedule", command=lambda : openaddselect())
bRemove.pack(side = TOP)
b2Remove = Button(buttonFrame2, text="Remove", command= lambda : openremoveselect())
b2Remove.pack(side = TOP)
b3Remove = Button(buttonFrame2, text="Add Block", command= lambda : openaddblockselect())
b3Remove.pack(side = TOP)
b4Remove = Button(buttonFrame2, text="Remove Block", command= lambda : openremoveblockselect())
b4Remove.pack(side = TOP)




# Menu Bar
menu = Menu(root)
root.config(menu = menu)

filemenu = Menu(menu)
updatemenu = Menu(menu)
schmenu = Menu(menu)
googlemenu = Menu(menu)

menu.add_cascade(label = "File", menu = filemenu)
menu.add_cascade(label = "Schedule", menu = schmenu)
menu.add_cascade(label = "Update", menu = updatemenu)
menu.add_cascade(label = "Google Survey", menu = googlemenu)

##File Menu
filemenu.add_command(label = "New Schedule", command=lambda : doNewSchedule())
filemenu.add_command(label = "Open Schedule", command = lambda: doOpenSchedule())
filemenu.add_separator()
filemenu.add_command(label = "Save Schedule", command = lambda : doSave(output))
filemenu.add_command(label = "Save Schedule As", command = lambda : doSaveAs())
filemenu.add_separator()
filemenu.add_command(label = "Export Email", command = lambda: export.doExportMail(output2 = output, d = d))
filemenu.add_command(label = "Export Susan", command = lambda: export.doExportSusan(output2 = output, d = d))
filemenu.add_command(label = "Export Linda", command = lambda: export.doExportLinda(output2 = output, d = d))
filemenu.add_command(label = "Export All", command = lambda: export.doExportAll(output2 = output, d = d))
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = doQuit)

## Schedule Menu
schmenu.add_command(label = "By Class", command = lambda : doByClass())
schmenu.add_command(label = "By Student", command = lambda : doByStudent())
schmenu.add_separator()
schmenu.add_command(label = "Automate (Fast)", command = lambda : doAutomateFast())
schmenu.add_command(label = "Automate (Best)", command = lambda : doAutomateFast())

## Update Menu
updatemenu.add_command(label = "Download Classes", command = lambda : doDownloadClasses())
updatemenu.add_command(label = "Update Class Worths", command = lambda : doUpdateClassWorth())
updatemenu.add_command(label = "Update Classes", command = lambda : doUpdateClasses())
updatemenu.add_command(label = "Update Students", command = lambda: doUpdateStudents())



## Google Survey Meny
googlemenu.add_command(label = "List Classes", command = lambda : doListClasses())
googlemenu.add_command(label = "List Professors", command = lambda : doListProfessors())



# Run at startup
#doNewSchedule()
import os
try:
	dir_path = os.path.join(os.environ['APPDATA'], 'TAScheduling')
except KeyError:
	dir_path = os.path.join(os.environ['HOME'], '.TAScheduling')
if not os.path.exists(dir_path):
	os.makedirs(dir_path)
globalvars.database_path = os.path.join(dir_path, 'tascheduling.db')
globalvars.mat_prefs_path = os.path.join(dir_path, 'student_preferences.npy')
globalvars.sec_sec_matrix_path = os.path.join(dir_path, 'section_section_matrix.npy')
globalvars.para_path = os.path.join(dir_path, 'parameters.txt')


sqlite3.connect(globalvars.database_path)
import errno
def make_sure_path_exists(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
make_sure_path_exists('data/')


root.mainloop()