# create section_section matrix


# run with downloadClasses and updateClasses
def matrix_sections():
	import sqlite3
	import numpy as np
<<<<<<< HEAD
	
	import globalvars
=======
	import globalvars
	
>>>>>>> master
	conn = sqlite3.connect(globalvars.database_path)
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
			conflicts = 0
			pref = 0
			pref2 = 0
			
			
			a = sections[i][0]
			b = sections[j][0]
			# time conflicts
			conflictsa = cur.execute('''SELECT COUNT(*) FROM Con_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (a, b) )
			conflictsa = cur.fetchall()
			conflictsa = conflictsa[0][0]
			conflictsb = cur.execute('''SELECT COUNT(*) FROM Con_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (b,a) )
			conflictsb = cur.fetchall()
			conflictsb = conflictsb[0][0]
			
			if int(conflictsa) > 0 or int(conflictsb) > 0:
				conflicts = max(int(conflictsa),int(conflictsb))
			conflicts = conflicts * -10000000
			
			# 
			prefa = cur.execute('''SELECT COUNT(*) FROM Pref_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (a, b) )
			prefa = cur.fetchall()[0][0]
			prefb = cur.execute('''SELECT COUNT(*) FROM Pref_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (b,a) )
			prefb = cur.fetchall()[0][0]
			if prefa > 0 or prefb > 0:
				pref = max(prefa, prefb)
			pref = pref * 2000
			
			pref2a = cur.execute('''SELECT COUNT(*) FROM Pref2_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (a, b) )
			pref2a = cur.fetchall()[0][0]
			pref2a = pref2a * 1000
			pref2b = cur.execute('''SELECT COUNT(*) FROM Pref2_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (b,a) )
			pref2b = cur.fetchall()[0][0]
			pref2b = pref2b * 1000
			if pref2a > 0 or pref2b > 0:
				pref2 = max(pref2a, pref2b)
			pref2 = pref2 * 2000
					
			mat_sections[i,j] = conflicts + pref + pref2
	
	#Writing CSV file
	np.savetxt("data/section_section_matrix.csv", mat_sections, delimiter=",")
	return(mat_sections)
 

# Stu_Sec preferences
# run with #UpdateStudent
def matrix_pref(d):
	import sqlite3
	import numpy as np
	import globalvars
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	students = cur.execute('SELECT DISTINCT StudentID FROM Students')
	students = cur.fetchall()
	mat_prefs = np.zeros((len(students), len(sections)))
	mat_prefs.flags.writeable = True
	
	
	
	for i in range(len(students)):
		message = "Getting Preferences for Student Number " + str(i + 1)
		d.set(message)
		for j in range(len(sections)):
			# init values
			conflict1 = 0
			conflict2 = 0
			conflict3 = 0
			conflict4 = 0
			pref1 = 0
			pref2 = 0
			pref3 = 0
			pref4 = 0
			
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
			conflict1 = conflict1 * 1
				
			
			# student section time conflicts (overlaps survey)
			cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Time A INNER JOIN Con_Time_Time B
							On A.TimeID = B.TimeID1
							INNER JOIN Sections_Times C
							ON B.TimeID2 = C.TimeID
							WHERE A.StudentID = ? and C.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict2a = cur.fetchone()[0]
			cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Time A INNER JOIN Con_Time_Time B
							On A.TimeID = B.TimeID1
							INNER JOIN Sections_Times C
							ON B.TimeID2 = C.TimeID
							WHERE A.StudentID = ? and C.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict2b = cur.fetchone()[0]
			if conflict2a > 0 or conflict2b > 0:
				conflict2 = -5000
			conflict2 = conflict2 * 1
			
			# Student class conflict desire
			conflict3 = cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Class A INNER JOIN Sections B
							On A.ClassID = B.ClassID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict3 = cur.fetchone()[0]
			if int(conflict3) > 0:
				conflict3 = -500
			conflict3 = conflict3 * 1
			
			# student professor conflict desire
			cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Prof A INNER JOIN Sections B
							On A.ProfessorID = B.ProfessorID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict4 = cur.fetchone()[0]
			if int(conflict4) > 0:
				conflict4 = -500
			conflict4 = conflict4 * 1
			
			# student section YDS prefs
			cur.execute('''SELECT Count(*)
							FROM Students A INNER JOIN Year B
							ON A.Year = B.Name
							INNER JOIN Sections_Year C
							ON B.PrimaryKey = C.YearID
							WHERE A.StudentID = ? AND C.SectionID = ?
							''',(students[i][0],sections[j][0]))
			prefyr = cur.fetchone()[0]
			prefyr = prefyr * 1000
			
			
			cur.execute('''SELECT Count(*)
							FROM Students A INNER JOIN Division B
							ON A.Division = B.Name
							INNER JOIN Sections_Division C
							ON B.PrimaryKey = C.DivisionID
							WHERE A.StudentID = ? AND C.SectionID = ?
							''',(students[i][0],sections[j][0]))
			prefdiv = cur.fetchone()[0]
			prefdiv = prefdiv * 5000
			
			
			cur.execute('''SELECT Count(*)
							FROM Students A INNER JOIN Year B
							ON A.Skill = B.Name
							INNER JOIN Sections_Skill C
							ON B.PrimaryKey = C.SkillID
							WHERE A.StudentID = ? AND C.SectionID = ?
							''',(students[i][0],sections[j][0]))
			prefsk = cur.fetchone()[0]
			prefsk = prefsk * 1000
			
			
			# student section time prefs (equal to survey)
			cur.execute('''SELECT COUNT(*)
							FROM Students A INNER JOIN Pref_Student_Time B
							ON A.StudentID = B.StudentID
							INNER JOIN Sections_Times C
							ON B.TimeID = C.TimeID
							WHERE A.StudentID = ? AND C.SectionID = ?''', (students[i][0], sections[j][0]))
			pref1 = cur.fetchone()[0]
			if int(pref1) > 0:
				pref1 = 500
			pref1 = pref1 * 1
			
			# student section time prefs (overlaps survey)
			cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Time A INNER JOIN Con_Time_Time B
							On A.TimeID = B.TimeID1
							INNER JOIN Sections_Times C
							ON B.TimeID2 = C.TimeID
							WHERE A.StudentID = ? and C.SectionID = ?''', (students[i][0],sections[j][0]))
			pref2a = cur.fetchone()[0]
			cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Time A INNER JOIN Con_Time_Time B
							On A.TimeID = B.TimeID2
							INNER JOIN Sections_Times C
							ON B.TimeID1 = C.TimeID
							WHERE A.StudentID = ? and C.SectionID = ?''', (students[i][0],sections[j][0]))
			pref2b = cur.fetchone()[0]
			if int(pref2a) > 0 or pref2b > 0:
				pref2 = max(pref2a, pref2b)
			pref2 = pref2 * 500
			
			
			
			
			# student section class prefs
			pref3 = cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Class A INNER JOIN Sections B
							On A.ClassID = B.ClassID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			pref3 = cur.fetchone()[0]
			if int(pref3) > 0:
				pref3 = 500
			pref3 = pref3 * 1
			
			
			pref4 = cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Prof A INNER JOIN Sections B
							On A.ProfessorID = B.ProfessorID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			pref4 = cur.fetchone()[0]
			if int(pref4) > 0:
				pref4 = 500
			pref4 = pref4 * 1
			
			#print students[i][0], sections[j][0]
			#print conflict1, conflict2, conflict3, conflict4, pref1, pref2, pref3, pref4, prefyr, prefdiv, prefsk
			mat_prefs[i,j] = conflict1 + conflict2 + conflict3 + conflict4 + pref1 + pref2 + pref3 + pref4 + prefyr + prefdiv + prefsk
			
			
	
	np.savetxt("data/student_preferences.csv", mat_prefs, delimiter=",")
	return(mat_prefs)



def section_index():
	import sqlite3
	import numpy as np
	import globalvars
	
	conn = sqlite3.connect(globalvars.database_path)
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
	import globalvars
	
	conn = sqlite3.connect(globalvars.database_path)
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
	import globalvars
	
	conn = sqlite3.connect(globalvars.database_path)
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
	import globalvars
	
	conn = sqlite3.connect(globalvars.database_path)
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

