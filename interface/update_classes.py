# Sections download and clean up

#https://udapps.nss.udel.edu/CoursesSearch/search-results?&term=2173&search_type=A&course_sec=CHEM&text_info=All&credit=Any&session=All&instrtn_mode=All&startat=2173CHEM465011

# Term is 2173
# insert term
#https://udapps.nss.udel.edu/CoursesSearch/search-results?term=2173&search_type=A&course_sec=CHEM&session=All&course_title=&instr_name=&text_info=All&instrtn_mode=All&time_start_hh=&time_start_ampm=&credit=Any&keyword=&subj_area_code=&college=


#filename = 'file:///Users/katiedaisey/Desktop/tascheduling/sections_example.html'


# Clean up Entries
class update_classes:
	def __init__(self, term):
		import csv
		import urllib2
		from bs4 import BeautifulSoup
		self.filename = 'https://udapps.nss.udel.edu/CoursesSearch/search-results?term=' + term + '&search_type=A&course_sec=CHEM&session=All&course_title=&instr_name=&text_info=All&instrtn_mode=All&time_start_hh=&time_start_ampm=&credit=Any&keyword=&subj_area_code=&college='
		self.outputname = 'listings.csv'
		
		self.records = []
		#Read HTML file into memory
		for index in range(2):
		    self.nextPage = self.filename
		    while self.nextPage is not 'None':
				try:
					self.response = urllib2.urlopen(self.nextPage)
					html = self.response.read()
					self.nextPage = self.next_page(html)
					self.my_parse(html)
				except:
					raise
				finally:
					try:
						self.response.close()
					except:
						raise
		
		#Writing CSV file
		with open(self.outputname, 'wb') as self.f:
			self.writer = csv.writer(self.f, lineterminator = '\n')
			self.writer.writerows(self.records)
		
	# add year, division, skill
	# default year prefs for classes
	def year(self, tds):
		# choices 1, 2, 3, 4, 5, any
		yr = []
		if "General" in tds[1]:
			yr = "123"
		else:
			yr = "any"
		yr = [yr]
		return(yr)
	
	# default division prefs for classes
	def division(self, tds):
		div = []
		if "Quantitative" in tds[1]:
			div = "A"
		elif "Instrumental" in tds[1]:
			div = "A"
		elif "Organic" in tds[1]:
			div = "O"
		elif "Bio" in tds[1]:
			div = "B"
		elif "Physical" in tds[1]:
			div = "P"
		elif "Inorganic" in tds[1]:
			div = "I"
		else:
			div = "any"
		div = [div]
		return(div)
	
	
	# default skill prefs for classes
	def skill(self, tds):
		sk = ["any"]
		return(sk)
	
	# insert year, division, skill in row
	def addYDStoRow(self, tds):
		yr = self.year(tds)
		div = self.division(tds)
		sk = self.skill(tds)
		newtds = []
		newtds = tds[0:2] + yr + div + sk + tds[2:]
		return(newtds)
	
	# clean up entries
	def clean(self, tds):
		for i in range(len(tds)):
			elem = tds[i]
			elem = elem.text.encode('utf-8')
			elem = elem.strip()
			tds[i] = elem
		if tds[5] != 'TBA' and tds[5] != '\xc2\xa0' and tds[5] != 'Canceled':
			time = tds[5].split('-')
			time[1] = time[1].lstrip()
			time = '- '.join(time)
			tds[5] = time
			
		tds[0] = tds[0].strip()
		tds[0] = tds[0].replace('\n','')
		tds[4] = tds[4].replace('\n','')
		indices = [0, 1, 4, 5, 7]
		tds = [tds[x] for x in indices]
		tds = self.addYDStoRow(tds)
		return(tds)
	
	
	# Check for next page
	def next_page(self, html):
		from bs4 import BeautifulSoup
		soup = BeautifulSoup(html, "lxml")
		divs = soup.find_all('div')
		nextPage = 'None'
		for div in divs:
			if nextPage == 'None':
				try:
					id = div['id']
					if id == 'nextPage':
						nextPage = div.a.get('href')
				except:
					continue
		if nextPage != 'None':
			nextPage = 'https://udapps.nss.udel.edu/CoursesSearch/' + nextPage
		return(nextPage)
		
	
	#Grab table from HTML
	def my_parse(self, html):
		from bs4 import BeautifulSoup
		soup = BeautifulSoup(html, "lxml")
		table = soup.find_all('table')[0]
		for tr in table.find_all('tr')[1:]:
			tds = tr.find_all('td')
			coursetype = tr.find_all('span')
			coursetype = coursetype[0].string
			if coursetype == 'LAB' or coursetype == 'DIS':
				tds = self.clean(tds)
				self.records.append(tds)
	

def deleteExtraRecords():
	import csv
	filename = 'listings.csv'
	shortname = []
	records = []
	for entry in open(filename):
		entry = entry.rstrip()
		first = entry.split(',')[0]
		if first not in shortname:
			shortname.append(first)
			records.append(entry)
	with open(filename, 'wb') as f:
		for row in records:
			f.write(row)
			f.write('\n')

	
