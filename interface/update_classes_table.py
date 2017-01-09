def update_classes_table():
	
	import sqlite3
	from datetime import datetime
	
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	
	# Make some fresh tables using executescript()
	cur.executescript('''
	DROP TABLE IF EXISTS Classes;
	DROP TABLE IF EXISTS Professors;
	DROP TABLE IF EXISTS Sections;
	DROP TABLE IF EXISTS Times;
	DROP TABLE IF EXISTS Sections_Times;
	DROP TABLE IF EXISTS Con_Time_Time;
	DROP TABLE IF EXISTS Pref_Section_Section;
	DROP TABLE IF EXISTS Pref2_Section_Section;
	DROP TABLE IF EXISTS Con_Section_Section;
	DROP TABLE IF EXISTS Year;
	DROP TABLE IF EXISTS Division;
	DROP TABLE IF EXISTS Skill;
	DROP TABLE IF EXISTS Sections_Year;
	DROP TABLE IF EXISTS Sections_Division;
	DROP TABLE IF EXISTS Sections_Skill;
	
	CREATE TABLE Classes (
		ClassID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		Name	TEXT NOT NULL,
		YearID	INTEGER DEFAULT 0,
		DivisionID	INTEGER DEFAULT 0,
		SkillID	INTEGER DEFAULT 0,
		ShortName	TEXT UNIQUE,
		Worth	REAL DEFAULT .5
	);
	
	CREATE TABLE Professors (
		ProfessorID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		Name	TEXT NOT NULL UNIQUE
	);
	
	CREATE TABLE Sections (
		SectionID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		Name	TEXT NOT NULL,
		ProfessorID	INTEGER NOT NULL,
		ClassID	INTEGER NOT NULL,
		StudentID INTEGER DEFAULT 0,
		Scheduled INTEGER DEFAULT 0
	);
	
	CREATE TABLE Times (
		Time	TEXT,
		Start	TEXT,
		End		TEXT,
		Day	TEXT,
		TimeID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE
	);
	
	CREATE TABLE Sections_Times (
		PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		SectionID	INTEGER NOT NULL,
		TimeID	INTEGER NOT NULL
	);
	
	CREATE TABLE Con_Time_Time (
		PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		TimeID1	INTEGER NOT NULL,
		TimeID2	INTEGER NOT NULL
	);
	
	CREATE TABLE Pref_Section_Section (
		PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		SectionID1	INTEGER NOT NULL,
		SectionID2	INTEGER NOT NULL
	);
	
	CREATE TABLE Pref2_Section_Section (
		PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		SectionID1	INTEGER NOT NULL,
		SectionID2	INTEGER NOT NULL
	);

	CREATE TABLE Con_Section_Section (
		PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		SectionID1	INTEGER NOT NULL,
		SectionID2	INTEGER NOT NULL
	);
	
	CREATE TABLE Year (
		PrimaryKey INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		Name	TEXT
	);
	
	CREATE TABLE Division (
		PrimaryKey INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		Name	TEXT
	);
	CREATE TABLE Skill (
		PrimaryKey INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		Name	TEXT
	);
	CREATE TABLE Sections_Year(
		PrimaryKey INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		SectionID	INTEGER NOT NULL,
		YearID	INTEGER NOT NULL
	);
		CREATE TABLE Sections_Division(
		PrimaryKey INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		SectionID	INTEGER NOT NULL,
		DivisionID	INTEGER NOT NULL
	);
		CREATE TABLE Sections_Skill(
		PrimaryKey INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		SectionID	INTEGER NOT NULL,
		SkillID	INTEGER NOT NULL
	)
	
	
	''')
	
	# create YDS
	years = [1,2,3,4,5,"any"]
	skill = [1,2,3,4,5,"any"]
	division = ["A", "B", "I", "O", "P", "any"]
	
	for i in range(6):
		cur.execute('INSERT OR IGNORE INTO Year (Name) VALUES(?)', (years[i],))
		cur.execute('INSERT OR IGNORE INTO Division (Name) VALUES(?)', (division[i],))
		cur.execute('INSERT OR IGNORE INTO Skill (Name) VALUES(?)', (skill[i],))
	
	
	# update from each row in listings.csv
	# as created by update_classes.py
	filename = 'listings.csv'
	for entry in open(filename):
		entry = entry.rstrip()
		entry = entry.split(',')
		
		# create and get ProfessorID
		if len(entry) == 9:
			professor = entry[7] + ', ' + entry[8]
			professor = professor[1:-1]
			cur.execute('''INSERT OR IGNORE INTO Professors (Name) VALUES(?)''', (professor,))
			cur.execute('SELECT ProfessorID FROM Professors WHERE Name = ?', (professor, ))
			ProfessorID = cur.fetchone()[0]
			conn.commit()
		
		if len(entry) == 8:
			if entry[7] != '\xc2\xa0':
				professor = entry[7].strip()
				cur.execute('''INSERT OR IGNORE INTO Professors (Name) VALUES ( ? )''', (str(professor), ) )
				cur.execute('SELECT ProfessorID FROM Professors WHERE Name = ?', (professor, ))
				ProfessorID = cur.fetchone()[0]
				conn.commit()
			
			if entry[7] == '\xc2\xa0':
				professor = 'Staff'
				cur.execute('''INSERT OR IGNORE INTO Professors (Name)
	        	VALUES ( ? )''', (str(professor), ) )
				cur.execute('SELECT ProfessorID FROM Professors WHERE Name = ?', (professor, ))
				ProfessorID = cur.fetchone()[0]
				conn.commit()
		
		# create and get ClassID
		if len(entry) > 8:
			classname = entry[1]
			classother = entry[0]
			shortname = classother[0:7]
			
			cur.execute('''INSERT OR IGNORE INTO Classes (Name, ShortName) 
			VALUES ( ?, ? )''', ( classname, shortname ) )
			cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ? ', (shortname, ))
			ClassID = cur.fetchone()[0]
			
			# create and get SectionID
			sectionnum = classother[7:10]
			
			
			cur.execute('''INSERT OR IGNORE INTO Sections 
			(Name, ProfessorID, ClassID) VALUES (?, ?, ?)''', (sectionnum,	ProfessorID, ClassID) )
			cur.execute('SELECT SectionID FROM Sections WHERE Name = ? and ClassID = ?', (sectionnum, ClassID))
			SectionID = cur.fetchone()[0]
			
			
			# get YDS
			year = entry[2]
			if '1' in year:
				cur.execute('INSERT OR IGNORE INTO Sections_Year (SectionID, YearID) VALUES (?, ?)', (SectionID, 1))
			elif '2' in year:
				cur.execute('INSERT OR IGNORE INTO Sections_Year (SectionID, YearID) VALUES (?, ?)', (SectionID, 2))
			elif '3' in year:
				cur.execute('INSERT OR IGNORE INTO Sections_Year (SectionID, YearID) VALUES (?, ?)', (SectionID, 3))
			elif '4' in year:
				cur.execute('INSERT OR IGNORE INTO Sections_Year (SectionID, YearID) VALUES (?, ?)', (SectionID, 4))
			elif '5' in year:
				cur.execute('INSERT OR IGNORE INTO Sections_Year (SectionID, YearID) VALUES (?, ?)', (SectionID, 5))
			else:
				cur.execute('INSERT OR IGNORE INTO Sections_Year (SectionID, YearID) VALUES (?, ?)', (SectionID, 6))
			
			
			
			div = entry[3]
			if 'A' in div:
				cur.execute('INSERT OR IGNORE INTO Sections_Division (SectionID, DivisionID) VALUES (?, ?)', (SectionID, 1))
			elif 'B' in div:
				cur.execute('INSERT OR IGNORE INTO Sections_Division (SectionID, DivisionID) VALUES (?, ?)', (SectionID, 2))
			elif 'I' in div:
				cur.execute('INSERT OR IGNORE INTO Sections_Division (SectionID, DivisionID) VALUES (?, ?)', (SectionID, 3))
			elif 'O' in div:
				cur.execute('INSERT OR IGNORE INTO Sections_Division (SectionID, DivisionID) VALUES (?, ?)', (SectionID, 4))
			elif 'P' in div:
				cur.execute('INSERT OR IGNORE INTO Sections_Division (SectionID, DivisionID) VALUES (?, ?)', (SectionID, 5))
			else:
				cur.execute('INSERT OR IGNORE INTO Sections_Division (SectionID, DivisionID) VALUES (?, ?)', (SectionID, 6))
			
			
			
			skill = entry[4]
			if '1' in skill:
				cur.execute('INSERT OR IGNORE INTO Sections_Skill (SectionID, SkillID) VALUES (?, ?)', (SectionID, 1))
			if '2' in skill:
				cur.execute('INSERT OR IGNORE INTO Sections_Skill (SectionID, SkillID) VALUES (?, ?)', (SectionID, 2))
			if '3' in skill:
				cur.execute('INSERT OR IGNORE INTO Sections_Skill (SectionID, SkillID) VALUES (?, ?)', (SectionID, 3))
			if '4' in skill:
				cur.execute('INSERT OR IGNORE INTO Sections_Skill (SectionID, SkillID) VALUES (?, ?)', (SectionID, 4))
			if '5' in skill:
				cur.execute('INSERT OR IGNORE INTO Sections_Skill (SectionID, SkillID) VALUES (?, ?)', (SectionID, 5))
			if '6' in skill:
				cur.execute('INSERT OR IGNORE INTO Sections_Skill (SectionID, SkillID) VALUES (?, ?)', (SectionID, 6))
			
			
			# create and get TimeID
			# clean up time entry
	
			time = entry[6]
			day = entry[5]
			try:
				end = time.split(' - ')[1].strip()
				start = time.split(' - ')[0].strip()
			except:
				start = 'TBA'
				end = 'TBA'
				time = 'TBA'
			cur.execute('SELECT TimeID FROM Times WHERE Time = ? and Day = ?', (time, day))
			try:
				data = cur.fetchone()[0]
			except:
				data = None
			if data is None:
				cur.execute('''INSERT OR IGNORE INTO Times (Start, End, Time, Day) VALUES (?, ?, ?, ?)''', (start, end, time, day))
				cur.execute('''SELECT TimeID FROM Times WHERE Time = ? and Day = ?''', (time, day))
				TimeID = cur.fetchone()[0]
			else:
				TimeID = data
				
			# Correspond section and time
			cur.execute('''INSERT OR IGNORE INTO Sections_Times (SectionID, TimeID) VALUES (?, ?)''', (SectionID, TimeID))
			
			
			
			
			
			conn.commit()
	
	
	
	
	# Determine Time_Time Conflicts
	days = ["M", "T", "W", "R", "F"]
	for day in days:
		times = cur.execute('''SELECT Start, End, TimeID FROM Times WHERE Day = ?''', (day, ) )
		#endtimes = cur.execute('''SELECT End FROM Times WHERE Day = ?''', (day, ) )
		id = []
		start = []
		end = []
		for time in times:
			start.append(datetime.strptime(str(time[0]), '%I:%M%p'))
			end.append(  datetime.strptime(str(time[1]), '%I:%M%p'))
			id.append(int(str(time[2])))
			
		for i in range(len(id)):
			otherstarts = start[:i] + start[i+1:]
			otherends = end[:i] + end[i+1:]
			otherids = id[:i] + id[i+1:]
			nowstart = start[i]
			nowend   = end[i]
			
			for j in range(len(otherstarts)):
				if nowstart > otherstarts[j] and nowstart < otherends[j]:
					cur.execute('''INSERT OR IGNORE INTO Con_Time_Time (TimeID1,
					 TimeID2) VALUES (?, ?)''', (id[i], otherids[j]) )
				elif nowend > otherstarts[j] and nowend < otherends[j]:
					cur.execute('''INSERT OR IGNORE INTO Con_Time_Time (TimeID1,
				 TimeID2) VALUES (?, ?)''', (id[i], otherids[j]) )
			conn.commit()
	
	
	# Determine Section_Section Preferences
	
	# preference for sections from same class
	classes = cur.execute('''SELECT DISTINCT ClassID FROM Sections''')
	classes = cur.fetchall()
	for course in classes:
		course = course[0]
		sections = cur.execute('''SELECT SectionID FROM Sections WHERE ClassID = ?''', (course, ) )
		sections = cur.fetchall()
		for i in range(len(sections)):
			othersections = sections[:i] + sections[i+1:]
			for j in range(len(othersections)):
					cur.execute('''INSERT OR IGNORE INTO Pref_Section_Section (SectionID1, SectionID2) VALUES (?, ?)''', (sections[i][0], othersections[j][0]))
		conn.commit()
		
	# preference for sections from same professor
	classes = cur.execute('''SELECT DISTINCT ProfessorID FROM Sections''')
	classes = cur.fetchall()
	for course in classes:
		course = course[0]
		sections = cur.execute('''SELECT SectionID FROM Sections WHERE ProfessorID = ?''', (course, ) )
		sections = cur.fetchall()
		for i in range(len(sections)):
			othersections = sections[:i] + sections[i+1:]
			for j in range(len(othersections)):
					cur.execute('''INSERT OR IGNORE INTO Pref2_Section_Section (SectionID1, SectionID2) VALUES (?, ?)''', (sections[i][0], othersections[j][0]))
		conn.commit()
	
	
	
	# Determine Section_Section Conflicts
	
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	for section in sections:
		section = section[0]
		conflict = cur.execute('''
			SELECT D.SectionID
			FROM Sections_Times B Inner Join Con_Time_Time C
			ON B.TimeID = C.TimeID1
			INNER JOIN Sections_Times D
			ON C.TimeID2 = D.TimeID
			WHERE B.SectionID = ?''', (section, ) )
		conflicts = cur.fetchall()
		if len(conflicts) > 0:
			for conflict in conflicts:
				cur.execute('''INSERT OR IGNORE INTO Con_Section_Section 
				(SectionID1, SectionID2) VALUES (?, ?)''', (section, conflict[0]))
		conn.commit()



