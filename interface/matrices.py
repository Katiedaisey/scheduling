# create section_section matrix


# run with downloadClasses and updateClasses
def matrix_sections():
	import sqlite3
	import numpy as np
	import globalvars
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
			conflicts = conflicts * globalvars.sec_time_con
			
			# same class name
			prefa = cur.execute('''SELECT COUNT(*) FROM Pref_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (a, b) )
			prefa = cur.fetchall()[0][0]
			prefb = cur.execute('''SELECT COUNT(*) FROM Pref_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (b,a) )
			prefb = cur.fetchall()[0][0]
			if prefa > 0 or prefb > 0:
				pref = max(prefa, prefb)
			pref = pref * globalvars.sec_sameclass_pref
			
			# same professor
			pref2a = cur.execute('''SELECT COUNT(*) FROM Pref2_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (a, b) )
			pref2a = cur.fetchall()[0][0]
			pref2b = cur.execute('''SELECT COUNT(*) FROM Pref2_Section_Section WHERE SectionID1 = ? AND SectionID2 = ?''', (b,a) )
			pref2b = cur.fetchall()[0][0]
			if pref2a > 0 or pref2b > 0:
				pref2 = max(pref2a, pref2b)
			pref2 = pref2 * globalvars.sec_sameprof_pref
					
			mat_sections[i,j] = conflicts + pref + pref2
	
	#Writing CSV file
	np.save(globalvars.sec_sec_matrix_path, mat_sections)
	globalvars.matrix_sections = mat_sections
	#np.savetxt("data/section_section_matrix.csv", mat_sections, delimiter=",")
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
				conflict1 = 1
			conflict1 = conflict1 * globalvars.stu_time_con
				
			
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
				conflict2 = 1
			conflict2 = conflict2 * globalvars.stu_time_con
			
			# Student class conflict desire
			conflict3 = cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Class A INNER JOIN Sections B
							On A.ClassID = B.ClassID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict3 = cur.fetchone()[0]
			if int(conflict3) > 0:
				conflict3 = 1
			conflict3 = conflict3 * globalvars.stu_class_con
			
			# student professor conflict desire
			cur.execute('''SELECT COUNT(*)
							FROM Con_Student_Prof A INNER JOIN Sections B
							On A.ProfessorID = B.ProfessorID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			conflict4 = cur.fetchone()[0]
			if int(conflict4) > 0:
				conflict4 = 1
			conflict4 = conflict4 * globalvars.stu_prof_con
			
			# student section YDS prefs
			cur.execute('''SELECT Count(*)
							FROM Students A INNER JOIN Year B
							ON A.Year = B.Name
							INNER JOIN Sections_Year C
							ON B.PrimaryKey = C.YearID
							WHERE A.StudentID = ? AND C.SectionID = ?
							''',(students[i][0],sections[j][0]))
			prefyr = cur.fetchone()[0]
			prefyr = prefyr * globalvars.stu_year_prof
			
			
			cur.execute('''SELECT Count(*)
							FROM Students A INNER JOIN Division B
							ON A.Division = B.Name
							INNER JOIN Sections_Division C
							ON B.PrimaryKey = C.DivisionID
							WHERE A.StudentID = ? AND C.SectionID = ?
							''',(students[i][0],sections[j][0]))
			prefdiv = cur.fetchone()[0]
			prefdiv = prefdiv * globalvars.stu_div_pref
			
			
			cur.execute('''SELECT Count(*)
							FROM Students A INNER JOIN Year B
							ON A.Skill = B.Name
							INNER JOIN Sections_Skill C
							ON B.PrimaryKey = C.SkillID
							WHERE A.StudentID = ? AND C.SectionID = ?
							''',(students[i][0],sections[j][0]))
			prefsk = cur.fetchone()[0]
			prefsk = prefsk globalvars.stu_skill.pref
			
			
			# student section time prefs (equal to survey)
			cur.execute('''SELECT COUNT(*)
							FROM Students A INNER JOIN Pref_Student_Time B
							ON A.StudentID = B.StudentID
							INNER JOIN Sections_Times C
							ON B.TimeID = C.TimeID
							WHERE A.StudentID = ? AND C.SectionID = ?''', (students[i][0], sections[j][0]))
			pref1 = cur.fetchone()[0]
			if int(pref1) > 0:
				pref1 = 1
			pref1 = pref1 * globalvars.stu_time_pref
			
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
				pref2 = 1
			pref2 = pref2 * stu_time_pref
			
			
			
			
			# student section class prefs
			pref3 = cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Class A INNER JOIN Sections B
							On A.ClassID = B.ClassID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			pref3 = cur.fetchone()[0]
			if int(pref3) > 0:
				pref3 = 1
			pref3 = pref3 * globalvars.stu_class_pref
			
			
			# student professor pref
			pref4 = cur.execute('''SELECT COUNT(*)
							FROM Pref_Student_Prof A INNER JOIN Sections B
							On A.ProfessorID = B.ProfessorID
							WHERE A.StudentID = ? and B.SectionID = ?''', (students[i][0],sections[j][0]))
			pref4 = cur.fetchone()[0]
			if int(pref4) > 0:
				pref4 = 1
			pref4 = pref4 * globalvars.stu_prof_pref
			
			#print students[i][0], sections[j][0]
			#print conflict1, conflict2, conflict3, conflict4, pref1, pref2, pref3, pref4, prefyr, prefdiv, prefsk
			mat_prefs[i,j] = conflict1 + conflict2 + conflict3 + conflict4 + pref1 + pref2 + pref3 + pref4 + prefyr + prefdiv + prefsk
			
			
	
	np.save(globalvars.mat_prefs_path, mat_prefs)
	globalvars.mat_prefs = mat_prefs
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

