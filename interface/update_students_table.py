def update_students_table(filename, d):
    # update student tables
    import sqlite3
    from datetime import datetime
    import globalvars

    conn = sqlite3.connect(globalvars.database_path)

    def split_names(entry):
        fs = entry.split(', ')
        cs = list()
        while len(fs) > 0:
            if fs[0] == 'tba':
                c = '\"' + fs[0] + '\"'
                cs.append(c)
                fs = fs[1:]
            elif fs[0] == 'taf':
                c = 'S' + fs[0] + 'f'
                cs.append(c)
                fs = fs[1:]
            else:
                c = '\"' + str(fs[0]) + ', ' + str(fs[1]) + '\"'
                cs.append(c)
                fs = fs[2:]
        return (cs)

    import globalvars
    conn = sqlite3.connect(globalvars.database_path)
    cur = conn.cursor()

    # Make some fresh tables using executescript()
    cur.executescript('''
    DROP TABLE IF EXISTS Students;
    DROP TABLE IF EXISTS Con_Student_Time;
    DROP TABLE IF EXISTS Pref_Student_Time;
    DROP TABLE IF EXISTS Con_Student_Class;
    DROP TABLE IF EXISTS Pref_Student_Class;
    DROP TABLE IF EXISTS Con_Student_Prof;
    DROP TABLE IF EXISTS Pref_Student_Prof;
    
    
    CREATE TABLE Students (
        StudentID	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Name	TEXT NOT NULL,
        Email	TEXT NOT NULL,
        ID		TEXT,
        Year	INTEGER DEFAULT 0,
        Division	TEXT,
        Skill	INTEGER DEFAULT 0,
        Scheduled REAL DEFAULT 0
    );
    
    CREATE TABLE Pref_Student_Time (
        PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        StudentID	INTEGER NOT NULL,
        TimeID		INTEGER NOT NULL
    );
    
    CREATE TABLE Con_Student_Time (
        PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        StudentID	INTEGER NOT NULL,
        TimeID		INTEGER NOT NULL
    );
    
    CREATE TABLE Con_Student_Class (
        PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        StudentID	INTEGER NOT NULL,
        ClassID		INTEGER NOT NULL
    );
    
    CREATE TABLE Pref_Student_Class (
        PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        StudentID	INTEGER NOT NULL,
        ClassID		INTEGER NOT NULL
    );
    
    CREATE TABLE Con_Student_Prof (
        PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        StudentID	INTEGER NOT NULL,
        ProfessorID		INTEGER NOT NULL
    );
    
    CREATE TABLE Pref_Student_Prof (
        PrimaryKey	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        StudentID	INTEGER NOT NULL,
        ProfessorID		INTEGER NOT NULL
    );
    ''')

    skiprow = 0
    count = 0
    for entry in open(filename):
        message = "Updating Student Number " + str(count + 1)
        d.set(message)
        if skiprow > 0:
            # update student information
            entry = entry.split('\t')

            year = entry[4]
            if year == '1st':
                year = 1
            elif year == '2nd':
                year = 2
            elif year == '3rd':
                year = 3
            elif year == '4th':
                year = 4
            elif year == '5th and above':
                year = 5
            entry[4] = year

            div = entry[5][0]

            sk = entry[6]

            cur.execute(
                'INSERT OR IGNORE INTO Students (Name, Email, ID, Year, 	Division, Skill) VALUES (?, ?, ?, ?, ?, ?)',
                (entry[2], entry[1], entry[3], year, div, sk))
            cur.execute('SELECT StudentID FROM STUDENTS WHERE Name = ?', (entry[2],))
            StudentID = cur.fetchone()[0]

            # update student availability
            avails = entry[9]
            if len(avails) > 0:
                avails = avails.split(', ')
                for avail in avails:
                    avail = avail.split(' ')
                    day = avail[0]
                    if day == 'Monday':
                        day = 'M'
                    elif day == 'Tuesday':
                        day = 'T'
                    elif day == 'Wednesday':
                        day = 'W'
                    elif day == 'Thursday':
                        day = 'R'
                    elif day == 'Friday':
                        day = 'F'
                    elif day == 'Saturday':
                        day = 'S'
                    elif day == 'Sunday':
                        day = 'N'
                    time = avail[1]
                    start = time.split('-')
                    end = start[1]
                    start = start[0]
                    time = str(start) + ' - ' + str(end)
                    cur.execute('SELECT TimeID FROM Times WHERE Time = ? AND Day = ?', (time, day))
                    try:
                        data = cur.fetchone()[0]
                    except:
                        data = None
                    if data is None:
                        cur.execute('''INSERT OR IGNORE INTO Times (Start, End, Time, Day) VALUES (?, ?, ?, ?)''',
                                    (start, end, time, day))
                        cur.execute('''SELECT TimeID FROM Times WHERE Time = ? AND Day = ?''', (time, day))
                        TimeID = cur.fetchone()[0]
                    else:
                        TimeID = data
                    cur.execute('INSERT OR IGNORE INTO Pref_Student_Time (StudentID, TimeID) VALUES (?, ?)',
                                (StudentID, TimeID))
            conn.commit()

            # update student nonavailablility
            notavails = entry[7]
            if len(notavails) > 0:
                notavails = notavails.split(', ')
                for notavail in notavails:
                    notavail = notavail.split(' ')
                    day = notavail[0]
                    if day == 'Monday':
                        day = 'M'
                    elif day == 'Tuesday':
                        day = 'T'
                    elif day == 'Wednesday':
                        day = 'W'
                    elif day == 'Thursday':
                        day = 'R'
                    elif day == 'Friday':
                        day = 'F'
                    elif day == 'Saturday':
                        day = 'S'
                    elif day == 'Sunday':
                        day = 'N'
                    time = notavail[1]
                    start = time.split('-')
                    end = start[1]
                    start = start[0]
                    time = str(start) + ' - ' + str(end)
                    cur.execute('SELECT TimeID FROM Times WHERE Time = ? AND Day = ?', (time, day))
                    try:
                        data = cur.fetchone()[0]
                    except:
                        data = None
                    if data is None:
                        cur.execute('''INSERT OR IGNORE INTO Times (Start, End, Time, Day) VALUES (?, ?, ?, ?)''',
                                    (start, end, time, day))
                        cur.execute('''SELECT TimeID FROM Times WHERE Time = ? AND Day = ?''', (time, day))
                        TimeID = cur.fetchone()[0]
                    else:
                        TimeID = data
                    cur.execute('INSERT OR IGNORE INTO Con_Student_Time (StudentID, TimeID) VALUES (?, ?)',
                                (StudentID, TimeID))

            # student_class preference
            if len(entry[10]) > 0:
                classes = entry[10].split(', ')
                for clas in classes:
                    clas = clas.split(' - ')
                    clas = clas[0]
                    try:
                        cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?', (clas,))
                        ClassID = cur.fetchone()[0]
                        cur.execute('''INSERT OR IGNORE INTO Pref_Student_Class (StudentID, ClassID) VALUES (?,?)''',
                                    (StudentID, ClassID))
                    except:
                        continue

            # student_class nonprefence
            if len(entry[11]) > 0:
                classes = entry[11].split(', ')
                for clas in classes:
                    clas = clas.split(' - ')
                    clas = clas[0]
                    try:
                        cur.execute('SELECT ClassID FROM Classes WHERE ShortName = ?', (clas,))
                        ClassID = cur.fetchone()[0]
                        cur.execute('''INSERT OR IGNORE INTO Con_Student_Class (StudentID, ClassID) VALUES (?,?)''',
                                    (StudentID, ClassID))
                    except:
                        continue

            # student_prof preference
            if len(entry[12]) > 0:
                classes = split_names(entry[12])
                for clas in classes:
                    try:
                        cur.execute('SELECT ProfessorID FROM Professors WHERE Name = ?', (clas,))
                        ProfID = cur.fetchone()[0]
                        cur.execute('''INSERT OR IGNORE INTO Pref_Student_Prof (StudentID, ProfessorID) VALUES (?,?)''',
                                    (StudentID, ProfID))
                    except:
                        continue

            # student_prof nonprefence
            if len(entry[13]) > 0:
                classes = split_names(entry[13])
                for clas in classes:
                    try:
                        cur.execute('SELECT ProfessorID FROM Professors WHERE Name = ?', (clas,))
                        ProfID = cur.fetchone()[0]
                        cur.execute('''INSERT OR IGNORE INTO Con_Student_Prof (StudentID, ProfessorID) VALUES (?,?)''',
                                    (StudentID, ProfID))
                    except:
                        continue

            conn.commit()

        skiprow = skiprow + 1
    conn.commit()

    # Determine Time_Time Conflicts
    message = "Tidying Up"
    d.set(message)
    days = ["M", "T", "W", "R", "F", "S", "N"]
    for day in days:
        times = cur.execute('''SELECT Start, End, TimeID FROM Times WHERE Day = ?''', (day,))
        # endtimes = cur.execute('''SELECT End FROM Times WHERE Day = ?''', (day, ) )
        id = []
        start = []
        end = []
        for time in times:
            start.append(datetime.strptime(str(time[0]), '%I:%M%p'))
            end.append(datetime.strptime(str(time[1]), '%I:%M%p'))
            id.append(int(str(time[2])))

        for i in range(len(id)):
            otherstarts = start[:i] + start[i + 1:]
            otherends = end[:i] + end[i + 1:]
            otherids = id[:i] + id[i + 1:]
            nowstart = start[i]
            nowend = end[i]

            for j in range(len(otherstarts)):
                if nowstart > otherstarts[j] and nowstart < otherends[j]:
                    cur.execute('''INSERT OR IGNORE INTO Con_Time_Time (TimeID1,
                     TimeID2) VALUES (?, ?)''', (id[i], otherids[j]))
                    cur.execute('''INSERT OR IGNORE INTO Con_Time_Time (TimeID1,
                     TimeID2) VALUES (?, ?)''', (otherids[j], id[i]))
                elif nowend > otherstarts[j] and nowend < otherends[j]:
                    cur.execute('''INSERT OR IGNORE INTO Con_Time_Time (TimeID1,
                     TimeID2) VALUES (?, ?)''', (id[i], otherids[j]))
                    cur.execute('''INSERT OR IGNORE INTO Con_Time_Time (TimeID1,
                     TimeID2) VALUES (?, ?)''', (otherids[j], id[i]))
            conn.commit()

    # Determine Student_Class Preference and Conflicts
    students = cur.execute('SELECT DISTINCT StudentID FROM Students')
    students = cur.fetchall()
