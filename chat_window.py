#!/usr/bin/python
import queue, threading

from tkinter import *

class ChatWindow(Frame):
	#Definitions

	def __init__(self, p,output_q, output_l):
		self.parent = p
		Frame.__init__(self, self.parent)
		self.output_lock = output_l
		self.output_queue = output_q

		titulo = Label(self.parent, text = "Chat do Camilo, Alexandre e Pedro")

		chat = Frame(self.parent)
		scroll = Scrollbar(chat)
		self.chat_text = Text(chat, yscrollcommand=scroll.set)

		input_frame = Frame(self.parent)
		input_user = StringVar()
		input_field = Entry(input_frame, text=input_user)

		def on_click(*args):
			msg = input_field.get()
			if msg:
				# Blank messages are not allowed because they are intepreted as a request to close the socket
				self.send_msg(msg)
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
		self.parent.protocol('WM_DELETE_WINDOW', self.close)

		#Packing 
		titulo.pack(side=TOP, fill=X)

		chat.pack()
		scroll.pack(side=RIGHT, fill=Y)
		self.chat_text.pack(fill=BOTH)

		input_frame.pack(side=BOTTOM, fill=BOTH)
		send_button.pack(side=RIGHT)
		input_field.pack(side=LEFT, fill=BOTH, expand=True)

	def close(self):
		print("Closing")
		self.send_msg('')

	def send_msg(self, msg):
		self.output_lock.acquire()
		self.output_queue.put(msg)
		self.output_lock.release()

	def add_msg(self, msg):
		self.chat_text.config(state=NORMAL)
		self.chat_text.insert(INSERT, '%s\n' % msg)
		self.chat_text.config(state=DISABLED)

def main():
	window = Tk()
	ChatWindow(window).pack(side=TOP, fill=BOTH, expand=True)

	window.geometry("400x400+300+300")
	window.mainloop()

if __name__ == "__main__":
	main()