from Tkinter import *

class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()


if __name__ == "__main__":

    root = Tk()

    Frame(root, width=400, height=200).pack()
    status = StatusBar(root)
    status.pack(side=BOTTOM, fill=X)

    root.update()

    status.set("Connecting...")
    root.after(1000)
    status.set("Connected, logging in...")
    root.after(1500)
    status.set("Login accepted...")
    root.after(2000)
    status.clear()

    root.mainloop()