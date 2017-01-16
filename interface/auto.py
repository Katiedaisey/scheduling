import sqlite3
import numpy as np
import random
import os







def get_student_worth(stu):
	worth = amount[stu]
	return(worth)

def set_student_worth(stu, sec):
	import globalvars
	
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	stu_worth = cur.execute('SELECT Scheduled FROM Students')
	stu_worth = cur.fetchall()
	stu_worth[stu] = stu_worth[stu] + sec_worth[sec]

def get_section_worth(sec):
	import globalvars
	
	conn = sqlite3.connect(globalvars.database_path)
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
		if m[student] > 0:
			classes = mat_yes[student,:]
			cl = classes.tolist()
			cl = [i for i, x in enumerate(cl) if x==1]
			for c in cl:
				required[c] = classes
	return(required)
#m = get_require("output")


def get_require2(output):
	mat_yes = np.load(output + "/mat_yes.npy")
	#mat_no = np.load(output + "/mat_no.npy")
	m = np.sum(mat_yes, axis = 1)
	count = 0
	required = list()
	for student in range(len(m)):
		if m[student] > 0:
			classes = mat_yes[student,:]
			cl = classes.tolist()
			cl = [i for i, x in enumerate(cl) if x==1]
			required.append(cl)
	return(required)

#m = get_require2("interface/new")


def gen_sec_matrix(pop, keep, output):
	import sqlite3
	import numpy as np
	import random
	import os
	import globalvars
	
	
	conn = sqlite3.connect(globalvars.database_path)
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
	
	sec_prefs = np.genfromtxt('data/section_section_matrix.csv', delimiter=',')
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
	
	
	
	value = [None] * keep
	keepmat = [[None]] * keep
	count = 0
	for p in range(pop):
		mat_pos = np.copy(mat_base)
		left_third = base_third[:]
		left_half = base_half[:]
		left_single = base_single[:]
		
		
		# fill up "required" lines
		require2 = get_require2(output)
		for r in require2:
			worth = 0
			for c in r:
				worth = worth + sec_worth[c][0]
			
			# check if line is full
			#if worth > 0.9:
				#full
			
			if worth < 0.9 and worth > 0.59:
				# 2/3 sections
				# switch from random.choice to best possible left
				mpref =  sec_prefs[r[0],:] + sec_prefs[r[1],:]
				mpref = [i for i, j in enumerate(mpref) if j == max(mpref)]
				mpref = list(set(left_third).intersection(mpref))
				try:
					u = random.choice(mpref) # a best choice remains
				except:
					u = random.choice(left_third) # a lesser choice
				left_third.remove(u)
				
				for c in r:
					mat_pos[c,u] = 1
					mat_pos[u,c] = 1
			
			# 1/2 scheduled
			if worth > 0.49 and worth < 0.51:
				mpref = sec_prefs[r[0],:] # only class scheduled
				mpref = [i for i, j in enumerate(mpref) if j == max(mpref)]
				mpref = list(set(left_half).intersection(mpref))
				try:
					u = random.choice(mpref) # a best choice remains
				except:
					u = random.choice(left_half) # a lesser choice
				left_half.remove(u)
				for c in r:
					mat_pos[c,u] = 1
					mat_pos[u,c] = 1
			
			# 1/3 scheduled
			if worth > 0.25 and worth < 0.35:
				mpref = sec_prefs[r[0],:] # only class scheduled
				mpref = [i for i, j in enumerate(mpref) if j == max(mpref)]
				mpref = list(set(left_third).intersection(mpref))
				
				# get best two combo classes
				mprefmax = []
				listmprefmax = []
				for i in range(len(mpref)):
					leftmpref = mpref[:i] + mpref[i+1:]
					for j in range(len(leftmpref)):
						listmprefmax.append([mpref[i],leftmpref[j]])
						newmax = sec_prefs[r[0],mpref[i]] + sec_prefs[r[0],leftmpref[j]] + sec_prefs[mpref[i],leftmpref[j]]
						mprefmax.append(newmax)
				mpref = [i for i, j in enumerate(mprefmax) if j == max(mprefmax)]
				mpref = [listmprefmax[i] for i in mpref]
				try:
					u = random.choice(mpref)
					l1 = u[1]
					u = u[0]
					left_third.remove(u)
					left_third.remove(l1)
				except:
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
			
			mpref = sec_prefs[u,:] # only class scheduled
			mpref = [i for i, j in enumerate(mpref) if j == max(mpref)]
			mpref = list(set(left_third).intersection(mpref))
			
			# get best two combo classes
			mprefmax = []
			listmprefmax = []
			for i in range(len(mpref)):
				leftmpref = mpref[:i] + mpref[i+1:]
				for j in range(len(leftmpref)):
					listmprefmax.append([mpref[i],leftmpref[j]])
					newmax = sec_prefs[u,mpref[i]] + sec_prefs[u,leftmpref[j]] + sec_prefs[mpref[i],leftmpref[j]]
					mprefmax.append(newmax)
			mpref = [i for i, j in enumerate(mprefmax) if j == max(mprefmax)]
			mpref = [listmprefmax[i] for i in mpref]
			try:
				l1 = random.choice(mpref)
				l2 = l1[1]
				l1 = l1[0]
				left_third.remove(l1)
				left_third.remove(l2)
			except:
				l1 = random.choice(left_third)
				left_third.remove(l1)
				l2 = random.choice(left_third)
				left_third.remove(l2)
			
			mat_pos[u ,l1] = 1
			mat_pos[l1, u] = 1
			mat_pos[u ,l2] = 1
			mat_pos[l2, u] = 1
			mat_pos[l1,l2] = 1
			mat_pos[l2,l1] = 1
			
		
		while len(left_half) > 1:
			u = random.choice(left_half)
			left_half.remove(u)
			mpref = sec_prefs[u,:] # randomly chosen class
			mpref = [i for i, j in enumerate(mpref) if j == max(mpref)]
			mpref = list(set(left_half).intersection(mpref))
			try:
				l1 = random.choice(mpref) # a best choice remains
			except:
				l1 = random.choice(left_half) # a lesser choice
			left_half.remove(l1)
			
			mat_pos[ u,l1] = 1
			mat_pos[l1, u] = 1
		
		while len(left_single) > 0: # randomly choose a classe
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
		
		if newvalue > value[count] or value[count] is None:
			value[count] = newvalue
			keepmat[count] = mat_pos
			# keep 100 best matrices
			if count < (keep - 1):
				count = count + 1
			elif count == (keep - 1):
				count = 0
			
	np.save(output + '/best_sec_sec.npy', keepmat)
	return(keepmat)


#m = gen_sec_matrix(1,1, "output")






# generate set of sec_stu matrices
def gen_sec_stu_matrix(mat_prefs, pop, keep, mats, output):
	import sqlite3
	import numpy as np
	import random
	import os
	import globalvars
	
	
	conn = sqlite3.connect(globalvars.database_path)
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
	
	
	sec_prefs = np.genfromtxt('data/section_section_matrix.csv', delimiter=',')
	stu_sec_prefs = mat_prefs
	#stu_sec_prefs = np.genfromtxt('student_preferences.csv', delimiter = ',')
	
	
	# first scheduled students
	mat_yes = np.load(output + "/mat_yes.npy") # single section sch
	mat_add = np.load(output + "/mat_add.npy") # any section sch
	mat_no = np.load(output + "/mat_no.npy") # block
	m = np.sum(mat_yes, axis = 1)
	#mat_sch = mat_yes[:,:]
	#mat_sch.flags.writeable = True
	mat_base = np.copy(mat_yes)
	mat_base.flags.writeable = True
	
	
	
	value = [None] * keep
	keepmat = [[None]] * keep
	count = 0
	for m in range(mats):
		mat_base = np.copy(mat_yes)
		mat_sch = np.load(output + "/matrices/mat_" + str(m) + ".npy")
		# get students already scheduled
		count2 = 0
		base_stu = range(len(stu_worth))
		base_sec = range(len(sections))
		for s in stu_worth:
			# for rounding issues
			if s[0] > 0: #scheduled at all - already has line
				# count2 is student
				# need to get sections student has
				#mat_base[count2,:] = mat_sch[count2,:]
				
				# remove sections from list to be scheduled
				cl = [i for i, x in enumerate(mat_base[count2,:]) if x==1]
				# scheduled via single section
				if len(cl) > 0:
					
					# get line containing classes student is scheduled for
					# replace student schedule with line with additional classes
					mat_base[count2,:] = mat_sch[cl[0],:]
					base_stu.remove(count2)
					
					
				# any section, via mat_add, pref for class
				if len(cl) == 0:
					cl = [i for i, x in enumerate(mat_add[count2,:]) if x==1]
					cl = random.choice(cl)
					mat_base[count2,:] = mat_sch[cl,:]
					# get line containing classes student is scheduled for
				
				# remove classes scheduled
				cl = [i for i, x in enumerate(mat_base[count2,:]) if x==1]
				for c in cl:
					base_sec.remove(c)
				
			count2 = count2 + 1
		
		for p in range(pop):
			# get copy of matrix with already scheduled tas
			mat_sch1 = np.copy(mat_base)
			
			# make fresh copies of students and sections not hand scheduled
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
				
			# check that blocks in mat_no are statisfied
			m = mat_sch1 * mat_no
			m = np.sum(m)
			if m == 0: # no blocks were violated 
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
#prefs = np.load("output/mat_prefs.npy")
#gen_sec_stu_matrix(mat_prefs, pop, keep, mats, output)
#m = gen_sec_stu_matrix(prefs, 1, 1, 1, "output")

def break_up(output):
	import numpy as np
	import os
	matrices = np.load(output + "/best_sec_sec.npy")
	
	d = os.path.dirname(output + "/matrices/")
	

	if not os.path.exists(d):
		os.makedirs(d)
		
	count = 0
	for matrix in matrices:
		np.save(output + "/matrices/mat_" + str(count) + ".npy", matrix)
		count = count + 1

#break_up("output")

def break_up2(output):
	import numpy as np
	import os
	matrices = np.load(output + "/best_stu_sec.npy")
	
	d = os.path.dirname(output + "/matrices2/")
	

	if not os.path.exists(d):
		os.makedirs(d)
		
	count = 0
	for matrix in matrices:
		np.save(output + "/matrices2/mat_" + str(count) + ".npy", matrix)
		count = count + 1

#break_up2("output")

def updateDatabase(schedule, output, mat_pref):
	import globalvars
	import sqlite3
	import numpy as np
	
	
	conn = sqlite3.connect(globalvars.database_path)
	cur = conn.cursor()
	# reset student scheduled
	cur.execute('UPDATE Students SET Scheduled = ?', (0,))
	for sch in range(schedule.shape[1]):
		stu = [i for i, x in enumerate(schedule[:,sch]) if x==1]
		if len(stu) > 0:
			secworth = get_section_worth(sch)[0]
			cur.execute('UPDATE Sections SET Scheduled = ? WHERE SectionID = ?', (1, sch + 1))
			cur.execute('UPDATE Sections Set StudentID = ? WHERE SectionID = ?', (stu[0] + 1, sch + 1))
			
			cur.execute('SELECT Scheduled FROM Students WHERE StudentID = ?', (stu[0] + 1,))
			stuworth = cur.fetchone()[0]
			cur.execute('UPDATE Students SET Scheduled = ? WHERE StudentID = ?', (stuworth + secworth, stu[0] + 1))
		else:
			cur.execute('UPDATE Sections SET Scheduled = ? WHERE SectionID = ?', (0, sch + 1))
			cur.execute('UPDATE Sections Set StudentID = ? WHERE SectionID = ?', (0, sch + 1))
	conn.commit()
	#import numpy as np
	np.save(output + '/mat_prefs.npy', mat_pref)
#schedule = np.load('output/mat_yes.npy')
#m = updateDatabase(schedule)

#def revertDatabase(mat_yes):















