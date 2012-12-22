#! /usr/bin/python

from Tkinter import *

class MyApp:
	def __init__(self, parent):
		self.parent = parent
		self.f1 = Frame(parent)
		self.f1.pack()

		self.b1 = Button(self.f1, text='click', bg='blue')
		self.b1.pack(side=LEFT)
		self.b1.bind('<Button-1>', self.b1_left_click)
		self.b1.bind('<Return>', self.b1_left_click)

		self.b2 = Button(self.f1, text='goodbye!', background='red')
		self.b2.pack(side=LEFT)
		self.b2.bind('<Button-2>', self.b2_right_click)

	def b1_left_click(self, event):
		self.b1['text'] = self.b1['text'] + 'click'

	def b2_right_click(self, event):
		self.parent.destroy()

root = Tk()
myapp = MyApp(root)
root.mainloop()
