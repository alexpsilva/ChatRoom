#!/usr/bin/python
import queue, threading

from tkinter import *

class ChatWindow(Frame):
	#Definitions

	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		self.controller = controller

		titulo = Label(self, text = "Chat do Camilo, Alexandre e Pedro")

		chat_frame = Frame(self)
		scroll = Scrollbar(chat_frame)
		self.chat_text = Text(chat_frame, yscrollcommand=scroll.set)

		input_frame = Frame(self)
		input_user = StringVar()
		input_field = Entry(input_frame, text=input_user)

		def on_click(*args):
			msg = input_field.get()
			if msg:
				# Blank messages are not allowed because they are intepreted as a request to close the socket
				self.controller.send_msg(msg)
				input_user.set('')
				self.chat_text.see(END)
			return "break"

		def on_key(*args):
			# Disable the use of '\' because it is reserved for commands
			try:
				last_char = input_field.get()[-1]
			except:
				#(to-do) remove this
				print('Weird index out of range error')
			else:
				if last_char == '\ '[0]:
					input_user.set(input_field.get()[:-1])

		input_user.trace("w", on_key)
		input_field.bind("<Return>", on_click)
		send_button = Button(input_frame, text="Send", command=on_click)

		#Packing 
		titulo.pack(side=TOP, fill=X)

		chat_frame.pack()
		scroll.pack(side=RIGHT, fill=Y)
		self.chat_text.pack(fill=BOTH)

		input_frame.pack(side=BOTTOM, fill=BOTH)
		send_button.pack(side=RIGHT)
		input_field.pack(side=LEFT, fill=BOTH, expand=True)

	def recv_msg(self, msg):
		self.chat_text.config(state=NORMAL)
		self.chat_text.insert(INSERT, '%s\n' % msg)
		self.chat_text.config(state=DISABLED)

def main():
	window = Tk()
	ChatWindow(window, None, None, None).pack(side=TOP, fill=BOTH, expand=True)

	window.geometry("400x400+300+300")
	window.mainloop()

if __name__ == "__main__":
	main()