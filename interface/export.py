# Export Functions

def doExportMail(output2):
	import sqlite3
	
	conn = sqlite3.connect('data/ta_scheduling.db')
	cur = conn.cursor()
	cur.execute('SELECT StudentID FROM Students')
	students = cur.fetchall()
	
	rows = list()
	for stu in students:
		cur.execute('SELECT Email, Name From Students WHERE StudentID = ?', (stu[0],))
		
		info = cur.fetchone()
		info = info[0] + "\t" + info[1]
		c = cur.execute('''SELECT B.Name, C.ShortName, C.Name, 
		D.Name, E.Day, E.Time, B.Room
		FROM Sections B INNER JOIN Classes C 
		ON B.ClassID = C.ClassID 
		INNER JOIN Professors D 
		ON B.ProfessorID = D.ProfessorID 
		INNER JOIN Sections_Times F 
		ON B.SectionID = F.SectionID 
		INNER JOIN Times E 
		ON F.TimeID = E.TimeID 
		WHERE B.StudentID = ?''', (stu[0],))
		classes = cur.fetchall()
		
		allclasses = ""
		
		# format for .csv output
		for cl in classes:
			allclasses = allclasses + "\t" + cl[2] + "\t" + cl[1] + "\t" + cl[0] + "\t" + cl[3] + "\t" + cl[4] + "\t" + cl[5]
		rows.append(info + allclasses)
		
		
	# write to .csv
	filename = output2 + "/mailinglist.tsv"
	header = "Email\tStudent\tClass1(Long)\tClass1(Short)\tSection1\tProf1\tDay1\tTime1\tRoom1\tClass2(Long)\tClass2(Short)\tSection2\tProf2\tDay2\tTime2\tRoom2\tClass3(Long)\tClass3(Short)\tSection3\tProf3\tDay3\tTime3\tRoom3"
	print header
	with open(filename, 'wb') as f:
		f.write(header)
		f.write("\n")
		
		for row in rows:
			f.write(row)
			f.write("\n")
		f.close()
	message = "Data Exported for Susan"
	d.set(message)

#doExportMail("output")

def doExportSusan(output2):
	import sqlite3
	conn = sqlite3.connect('data/ta_scheduling.db')
	cur = conn.cursor()
	cur.execute('SELECT ClassID, ShortName FROM Classes')
	classes = cur.fetchall()
	
	for cl in classes:
		cur.execute('''SELECT B.Name, A.Name, A.ID
					FROM Sections B INNER JOIN Students A
					ON B.StudentID = A.StudentID
					WHERE B.ClassID = ?''', (cl[0],))
		secs = cur.fetchall()
		allsecs = ""
		for s in secs:
			allsecs = allsecs + s[1] + " (" + s[0] + ")" + "\t"
	
	filename = output2 + "/classeslist.tsv"
	with open(filename, 'wb') as f:
		for row in classes:
			f.write(row[1] + "\t" + allsecs)
			f.write("\n")
	f.close()
	message = "Data Exported for Susan"
	d.set(message)


def doExportLinda(output2):
	import sqlite3
	conn = sqlite3.connect('data/ta_scheduling.db')
	cur = conn.cursor()
	cur.execute('SELECT ClassID, ShortName FROM Classes')
	classes = cur.fetchall()
	
	for cl in classes:
		cur.execute('''SELECT B.Name, A.Name 
					FROM Sections B INNER JOIN Students A
					ON B.StudentID = A.StudentID
					WHERE B.ClassID = ?''', (cl[0],))
		secs = cur.fetchall()
		allsecs = ""
		for s in secs:
			allsecs = allsecs + s[1] + " (" + s[0] + ")" + "\t"
	
	filename = output2 + "/classeslist.tsv"
	with open(filename, 'wb') as f:
		for row in classes:
			f.write(row[1] + "\t" + allsecs)
			f.write("\n")
	f.close()
	message = "Data Exported for Linda"
	d.set(message)

#doExportLinda("output")


def doExportAll(output2, d):
	import sqlite3
	conn = sqlite3.connect('data/ta_scheduling.db')
	cur = conn.cursor()
	cur.execute('''SELECT A.Name, A.Email, A.Scheduled, A.Year, A.Division,
		A.Skill, B.Name, C.ShortName, C.Name, C.Worth, D.Name, E.Day, E.Time
		A.Skill, B.Name, C.ShortName, C.Name, C.Worth, D.Name, E.Day, E.Time,
		B.Room, B.NumberOpen, B.Seats 
		FROM Students A INNER JOIN Sections B 
		ON A.StudentID = B.StudentID
		INNER JOIN Classes C 
		ON B.ClassID = C.ClassID 
		INNER JOIN Professors D 
		ON B.ProfessorID = D.ProfessorID 
		INNER JOIN Sections_Times F 
		ON B.SectionID = F.SectionID 
		INNER JOIN Times E 
		ON F.TimeID = E.TimeID''')
	rows = cur.fetchall()
	
	
	filename = output2 + "/allschedule.tsv"
	with open(filename, 'wb') as f:
		f.write("TA Name\tEmail\tAmount Scheduled\tYear\tDivision\tSkill Level\tSection\tClass Name(Short)\tClass Name (Long)\tClass Worth\tProfessor Name\tDay\tTime\tRoom\tOpen Seats\tSeats\n")
		for row in rows:
			wr = ""
			for r in row:
				wr = wr + str(r) + "\t"
			f.write(wr)
			f.write("\n")
	f.close()
	message = "All Information Exported"
	d.set(message)




