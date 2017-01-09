filename = 'students.tsv'
skiprow = 0
count = 0
for entry in open(filename):
	if count < 2:
		print entry
		count = count + 1
		entry = entry.split('\t')
		c = 0
		for e in entry:
			print c, e
			c = c + 1