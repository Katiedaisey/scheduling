# create section_section matrix



def matrix_sections():
	import sqlite3
	import numpy as np
	import csv
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	
	# Section_Section conflicts and preferences
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	
	mat_sections = np.zeros((len(sections), len(sections)))
	mat_sections.flags.writeable = True
	
	
	#for i in range(len(sections)):
	#	for j in range(len(sections)):
	for i in range(len(sections)):
		for j in range(len(sections)):
			a = sections[i][0]
			b = sections[j][0]
			# time conflicts
			conflict = cur.execute('''SELECT COUNT(*) FROM Con_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (a, b) )
			conflicts = cur.fetchall()
			conflicts = conflicts[0][0]
			if int(conflicts) > 0:
				conflicts = -10000
			conflicts = conflicts
			
			#
			pref = cur.execute('''SELECT COUNT(*) FROM Pref_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (sections[i][0], sections[j][0]) )
			pref = cur.fetchall()[0][0]
			pref = pref * 1000
			
			pref2 = cur.execute('''SELECT COUNT(*) FROM Pref2_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (sections[i][0], sections[j][0]) )
			pref2 = cur.fetchall()[0][0]
			pref2 = pref2 * 1000
					
			mat_sections[i,j] = conflicts + pref + pref2
	#Writing CSV file
	np.savetxt("section_section_matrix.csv", mat_sections, delimiter=",")
	return(mat_sections)
 

# Stu_Sec preferences
def matrix_pref():
	import sqlite3
	import numpy as np
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	students = cur.execute('SELECT DISTINCT StudentID FROM Students')
	students = cur.fetchall()
	mat_prefs = np.zeros((len(students), len(sections)))
	mat_prefs.flags.writeable = True
	
	for i in range(len(students)):
		
		for j in range(len(sections)):
			
			# Student section time conflicts (equal to survey)
			conflict1 = cur.execute('''SELECT COUNT(*)
							FROM Students A INNER JOIN Con_Student_Time B
							ON A.StudentID = B.StudentID
							INNER JOIN Sections_Times C
							ON B.TimeID = C.TimeID
							WHERE A.StudentID = ? AND C.SectionID = ?''', (students[i][0], sections[j][0]))
			conflict1 = cur.fetchone()[0]
			if int(conflict1) > 0:
				conflict1 = -5000
			conflict1 = conflict1
			
			# student section time conflicts (overlaps survey)
			conflict2 = cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Time A INNER JOIN Con_Time_Time B
							On A.TimeID = B.TimeID1
							INNER JOIN Sections_Times C
							ON B.TimeID2 = C.TimeID
							WHERE A.StudentID = ? and C.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict2 = cur.fetchone()[0]
			if int(conflict2) > 0:
				conflict2 = -5000
			conflict2 = conflict2
			
			# Student class conflict desire
			conflict3 = cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Class A INNER JOIN Sections B
							On A.ClassID = B.ClassID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict3 = cur.fetchone()[0]
			if int(conflict3) > 0:
				conflict3 = -500
			conflict3 = conflict3
			
			# student professor conflict desire
			conflict4 = cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Prof A INNER JOIN Sections B
							On A.ProfessorID = B.ProfessorID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict4 = cur.fetchone()[0]
			if int(conflict4) > 0:
				conflict4 = -500
			conflict4 = conflict4
			
			# student section YDS prefs
			
			# student section time prefs (equal to survey)
			pref1 = cur.execute('''SELECT COUNT(*)
							FROM Students A INNER JOIN Pref_Student_Time B
							ON A.StudentID = B.StudentID
							INNER JOIN Sections_Times C
							ON B.TimeID = C.TimeID
							WHERE A.StudentID = ? AND C.SectionID = ?''', (students[i][0], sections[j][0]))
			pref1 = cur.fetchone()[0]
			if int(pref1) > 0:
				pref1 = 500
			
			# student section time prefs (overlaps survey)
			pref = cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Time A INNER JOIN Con_Time_Time B
							On A.TimeID = B.TimeID1
							INNER JOIN Sections_Times C
							ON B.TimeID2 = C.TimeID
							WHERE A.StudentID = ? and C.SectionID = ?''', (students[i][0],sections[j][0]))
			pref2 = cur.fetchone()[0]
			if int(pref2) > 0:
				pref2 = 500
			
			
			
			# student section class prefs
			pref3 = cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Class A INNER JOIN Sections B
							On A.ClassID = B.ClassID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			pref3 = cur.fetchone()[0]
			if int(pref3) > 0:
				pref3 = 500
			pref3 = pref3
			
			
			pref4 = cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Prof A INNER JOIN Sections B
							On A.ProfessorID = B.ProfessorID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			pref4 = cur.fetchone()[0]
			if int(pref4) > 0:
				pref4 = 500
			pref4 = pref4
			
			
			mat_prefs[i,j] = conflict1 + conflict2 + conflict3 + conflict4 + pref1 + pref2 + pref3 + pref4
			
	np.savetxt("student_preferences.csv", mat_prefs, delimiter=",")
	return(mat_prefs)


def section_index():
	import sqlite3
	import numpy as np
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	
	# Section_Section conflicts and preferences
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	s = {}
	for j in range(len(sections)):
		s[sections[j][0]] = j
	return(s)

def student_index():
	import sqlite3
	import numpy as np
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	
	# Section_Section conflicts and preferences
	sections = cur.execute('SELECT DISTINCT StudentID FROM Students')
	sections = cur.fetchall()
	s = {}
	for j in range(len(sections)):
		s[sections[j][0]] = j
	return(s)


def matrix_schedule_manual():
	import sqlite3
	import numpy as np
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	students = cur.execute('SELECT DISTINCT StudentID FROM Students')
	students = cur.fetchall()
	mat_sch = np.zeros((len(students), len(sections)))
	mat_sch.flags.writeable = True
	return(mat_sch)



def all_possible(manual):
	import sqlite3
	import numpy as np
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	students = cur.execute('SELECT DISTINCT StudentID FROM Students')
	students = cur.fetchall()
	mat_pos = np.zeros((len(students), len(sections)))
	mat_pos.flags.writeable = True
	mat_pos = np.add(mat_pos, manual)


	
#m = matrix_sections()
#matrix_pref()

