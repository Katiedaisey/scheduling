# update students and classes




def callUpdateClasses(master):
	import update_classes
	import sys
	
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='Enter 4 digit Code of Term:')
			self.myLabel.pack()
			self.myEntryBox = Entry(top)
			self.myEntryBox.pack()
			self.mySubmitButton = Button(top, text='Update', command=self.send)
			self.mySubmitButton.pack()
			
		def send(self):
			self.value = self.myEntryBox.get()
			self.top.destroy()
		
	def onClick():
	    inputDialog = MyDialog(master)
	    master.wait_window(inputDialog.top)
	    
	    return(inputDialog.value)
	
	a = onClick()
	update_classes(a)
	return(a)

def callUpdateStudents():
	return("Students updated!")
	
def callUpdateClasses():
	import update_classes
	import sys
	
	
	class MyDialog:
		
		def __init__(self, parent):
			top = self.top = Toplevel(parent)
			self.myLabel = Label(top, text='Enter 4 digit Code of Term:')
			self.myLabel.pack()
			self.myEntryBox = Entry(top)
			self.myEntryBox.pack()
			self.mySubmitButton = Button(top, text='Update', command=self.send)
			self.mySubmitButton.pack()
			
		def send(self):
			self.value = self.myEntryBox.get()
			self.top.destroy()
		
	def onClick():
	    inputDialog = MyDialog(root)
	    root.wait_window(inputDialog.top)
	    
	    return(inputDialog.value)
	
	a = onClick()
	return(a)