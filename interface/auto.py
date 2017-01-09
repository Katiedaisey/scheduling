import sqlite3
import numpy as np
import random
import os







def get_student_worth(stu):
	worth = amount[stu]
	return(worth)

def set_student_worth(stu, sec):
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	stu_worth = cur.execute('SELECT Scheduled FROM Students')
	stu_worth = cur.fetchall()
	stu_worth[stu] = stu_worth[stu] + sec_worth[sec]

def get_section_worth(sec):
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	sec_worth = cur.execute('SELECT A.Worth FROM Classes A INNER JOIN Sections B ON A.ClassID = B.ClassID')
	sec_worth = cur.fetchall()
	worth = sec_worth[sec]
	return(worth)


# currently only does positive requirements
# currently by number of classes (ie > 1)
# switch to student worth
def get_require(output):
	mat_yes = np.load(output + "/mat_yes.npy")
	#mat_no = np.load(output + "/mat_no.npy")
	m = np.sum(mat_yes, axis = 1)
	required = dict()
	for student in range(len(m)):
		if m[student] > 1:
			classes = mat_yes[student,:]
			cl = classes.tolist()
			cl = [i for i, x in enumerate(cl) if x==1]
			for c in cl:
				required[c] = classes
	return(required)
#m = get_require("interface/new")


def get_require2(output):
	mat_yes = np.load(output + "/mat_yes.npy")
	#mat_no = np.load(output + "/mat_no.npy")
	m = np.sum(mat_yes, axis = 1)
	count = 0
	required = list()
	for student in range(len(m)):
		if m[student] > 1:
			classes = mat_yes[student,:]
			cl = classes.tolist()
			cl = [i for i, x in enumerate(cl) if x==1]
			required.append(cl)
	return(required)

#m = get_require2("interface/new")


def gen_sec_matrix(pop, keep, output):
	
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	stu_worth = cur.execute('SELECT Scheduled FROM Students')
	stu_worth = cur.fetchall()
	sec_worth = cur.execute('SELECT A.Worth FROM Classes A INNER JOIN Sections B ON A.ClassID = B.ClassID')
	sec_worth = cur.fetchall()
	
	mat_base = np.zeros((len(sections), len(sections)))
	np.fill_diagonal(mat_base, 1)
	mat_base.flags.writeable = True
	
	sec_prefs = np.genfromtxt('section_section_matrix.csv', delimiter=',')
	#stu_sec_prefs = np.genfromtxt('student_preferences.csv', delimiter = ',')
	
	
	
	# get columns where mat_hard is already scheduled
	#hard = get_cols(mat_hard)
	base = range(len(sections))
	
	# split sec into parts by worth
	base_third = [i for i, x in enumerate(sec_worth) if x[0] > 0.29 and x[0] < 0.35]
	base_half = [i for i, x in enumerate(sec_worth) if x[0] > 0.49 and x[0] < 0.51]
	base_single = [i for i, x in enumerate(sec_worth) if x[0] ==1]
	
	# hard coded positive restrictions
	require = get_require(output)
	for r in require:
		mat_base[(r),:] = require[r]
		mat_base[:,(r)] = require[r]
		
		if sec_worth[r][0] > 0.29 and sec_worth[r][0] < 0.35:
			base_third.remove(r)
		if sec_worth[r][0] > 0.49 and sec_worth[r][0] < 0.51:
			base_half.remove(r)
		if sec_worth[r][0] > 0.9:
			base_single.remove(r)
	
	
	
	
	value = [0] * keep
	keepmat = [[0]] * keep
	count = 0
	for p in range(pop):
		mat_pos = np.copy(mat_base)
		left_third = base_third[:]
		left_half = base_half[:]
		left_single = base_single[:]
		
		
		# fill up "required" lines
		require = get_require2(output)
		for r in require:
			worth = 0
			for c in r:
				worth = worth + sec_worth[c][0]
			
			
			# check if line is full
			#if worth > 0.9:
				#full
			
			if worth < 0.9 and worth > 0.59:
				# 2/3 sections
				u = random.choice(left_third)
				left_third.remove(u)
				
				for c in r:
					mat_pos[c,u] = 1
					mat_pos[u,c] = 1
			
			# 1/2 scheduled
			if worth > 0.49 and worth < 0.51:
				u = random.choice(left_half)
				left_half.remove(u)
				for c in r:
					mat_pos[c,u] = 1
					mat_pos[u,c] = 1
			
			# 1/3 scheduled
			if worth > 0.25 and worth < 0.35:
				u = random.choice(left_third)
				left_third.remove(u)
				l1 = random.choice(left_third)
				left_third.remove(u)
				
				for c in r:
					mat_pos[c,u] = 1
					mat_pos[c,l1] = 1
					mat_pos[u,c] = 1
					mat_pos[l1,c] = 1
				mat_pos[u,l1] = 1
				mat_pos[l1,u] = 1
		
		
		
		# schedule full ta lines
		while len(left_third) > 2:
			
			u = random.choice(left_third)
			left_third.remove(u)
			l1 = random.choice(left_third)
			left_third.remove(l1)
			l2 = random.choice(left_third)
			left_third.remove(l2)
			
			
			mat_pos[u,l1] = 1
			mat_pos[u,l2] = 1
			mat_pos[l1,u] = 1
			mat_pos[l1,l2] = 1
			mat_pos[l2,u] = 1
			mat_pos[l2,l1] = 1
		
		while len(left_half) > 1:
			
			u = random.choice(left_half)
			left_half.remove(u)
			l1 = random.choice(left_half)
			left_half.remove(l1)
			
			
			
			mat_pos[u,l1] = 1
			mat_pos[l1,u] = 1
		
		while len(left_single) > 0:
			u = random.choice(left_single)
			left_single.remove(u)
			
			
		
		# if 2/3 worth left, create line
		if len(left_third) > 1:
			u = random.choice(left_third)
			left_third.remove(u)
			l1 = random.choice(left_third)
			left_third.remove(l1)
			
			mat_pos[u,l1] = 1
			mat_pos[l1,u] = 1
		
		# if 1/3 and 1/2 left over, make line
		if len(left_third) == 1 and len(left_half) == 1:
			u = random.choice(left_third)
			left_third.remove(u)
			l1 = random.choice(left_half)
			left_half.remove(l1)
			
			mat_pos[u,l1] = 1
			mat_pos[l1,u] = 1
			
		# if 1/2 left over, make line
		if len(left_half) == 1:
			u = random.choice(left_half)
			left_half.remove(u)
		
		newmat = mat_pos * sec_prefs # element wise multiplication
		newvalue = sum(sum(newmat))
		
		if newvalue > value[count]:
			value[count] = newvalue
			keepmat[count] = mat_pos
			# keep 100 best matrices
			if count < (keep - 1):
				count = count + 1
			elif count == (keep - 1):
				count = 0
			
	np.save(output + '/best_sec_sec.npy', keepmat)
	return(keepmat)


#m = gen_sec_matrix(1000,100, "output")






# generate set of sec_stu matrices
def gen_sec_stu_matrix(mat_prefs, pop, keep, mats, output):
	
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	sections = cur.execute('SELECT DISTINCT SectionID FROM Sections')
	sections = cur.fetchall()
	stu_worth = cur.execute('SELECT Scheduled FROM Students')
	stu_worth = cur.fetchall()
	sec_worth = cur.execute('SELECT A.Worth FROM Classes A INNER JOIN Sections B ON A.ClassID = B.ClassID')
	sec_worth = cur.fetchall()
	
	mat_base = np.zeros((len(sections), len(sections)))
	np.fill_diagonal(mat_base, 1)
	mat_base.flags.writeable = True
	
	
	sec_prefs = np.genfromtxt('section_section_matrix.csv', delimiter=',')
	stu_sec_prefs = mat_prefs
	#stu_sec_prefs = np.genfromtxt('student_preferences.csv', delimiter = ',')
	
	
	# first scheduled students
	mat_yes = np.load(output + "/mat_yes.npy")
	#mat_no = np.load(output + "/mat_no.npy")
	m = np.sum(mat_yes, axis = 1)
	#mat_sch = mat_yes[:,:]
	#mat_sch.flags.writeable = True
	mat_base = np.copy(mat_yes)
	mat_base.flags.writeable = True
	
	
	
	
	value = [None] * keep
	keepmat = [[None]] * keep
	count = 0
	for m in range(mats):
		mat_sch = np.load(output + "/matrices/mat_" + str(m) + ".npy")
		# get students already scheduled
		count2 = 0
		base_stu = range(len(stu_worth))
		base_sec = range(len(sections))
		for s in stu_worth:
			# for rounding issues
			if s[0] > 0: #scheduled at all - already has line
				base_stu.remove(count2)
				mat_base[count2,:] = mat_sch[count2,:]
				cl = [i for i, x in enumerate(mat_sch[count2,:]) if x==1]
				for c in cl:
					base_sec.remove(c)
			count2 = count2 + 1
		for p in range(pop):
			mat_sch1 = np.copy(mat_base)
			left_stu = base_stu[:]
			left_sec = base_sec[:]
			while len(left_stu) > 0 and len(left_sec) > 0:
				stu = random.choice(left_stu)
				left_stu.remove(stu)

				# get ta line for student
				l = random.choice(left_sec)
				classes = mat_sch[l,:]
				
				mat_sch1[stu,:] = classes
				cl = classes.tolist()
				cl = [i for i, x in enumerate(cl) if x==1]
				for c in cl:
					#set_student_worth(stu, c)
					try:
						left_sec.remove(c)
					except:
						continue
				
				
			
			newmat = mat_sch1 * stu_sec_prefs # element wise multiplication
			newvalue = sum(sum(newmat))
			
			if newvalue > value[count] or value[count] is None:
				value[count] = newvalue
				keepmat[count] = mat_sch1
				# keep only best matrices
				if count < (keep - 1):
					count = count + 1
				elif count == (keep - 1):
					count = 0
			
	np.save(output + '/best_stu_sec.npy', keepmat)
	return(keepmat)

#import numpy as np
#prefs = np.load("test1/mat_prefs.npy")
#m = gen_sec_stu_matrix(prefs, 100, 1, 1, "test1")

def break_up(output):
	matrices = np.load(output + "/best_sec_sec.npy")
	
	d = os.path.dirname(output + "/matrices/")
	

	if not os.path.exists(d):
		os.makedirs(d)
		
	count = 0
	for matrix in matrices:
		np.save(output + "/matrices/mat_" + str(count) + ".npy", matrix)
		count = count + 1

#break_up("test1")
def updateDatabase(schedule, output, mat_pref):
	conn = sqlite3.connect('/Users/katiedaisey/Desktop/tascheduling/try1.db')
	cur = conn.cursor()
	# reset student scheduled
	cur.execute('UPDATE Students SET Scheduled = ?', (0,))
	for sch in range(schedule.shape[1]):
		stu = [i for i, x in enumerate(schedule[:,sch]) if x==1]
		if len(stu) > 0:
			secworth = get_section_worth(sch + 1)[0]
			cur.execute('UPDATE Sections SET Scheduled = ? WHERE SectionID = ?', (1, sch + 1))
			cur.execute('UPDATE Sections Set StudentID = ? WHERE SectionID = ?', (stu[0] + 1, sch + 1))
			
			cur.execute('SELECT Scheduled FROM Students WHERE StudentID = ?', (stu[0] + 1,))
			stuworth = cur.fetchone()[0]
			cur.execute('UPDATE Students SET Scheduled = ? WHERE StudentID = ?', (stuworth + secworth, stu[0] + 1))
		else:
			cur.execute('UPDATE Sections SET Scheduled = ? WHERE SectionID = ?', (0, sch + 1))
			cur.execute('UPDATE Sections Set StudentID = ? WHERE SectionID = ?', (0, sch + 1))
	conn.commit()
	import numpy as np
	np.save(output + '/mat_prefs.npy', mat_pref)
#schedule = np.load('output/mat_yes.npy')
#m = updateDatabase(schedule)

#def revertDatabase(mat_yes):















