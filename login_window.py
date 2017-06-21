from tkinter import *

class LoginWindow(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.input_username = StringVar()
		username_label = Label(self, text = "Username")
		username_label.grid(row=1, sticky=W)
		username_entry = Entry(self, text=self.input_username)
		username_entry.grid(row=1, column=1)

		self.input_password = StringVar()
		password_label = Label(self, text = "Password")
		password_label.grid(row=2, sticky=W)
		password_entry = Entry(self, show='*', text=self.input_password)
		password_entry.grid(row=2, column=1)

		def on_key_username(*args):
			# Disable the use of '\' because it is reserved for commands
			try:
				last_char = self.input_username.get()[-1]
			except:
				#(to-do) remove this
				print('Weird index out of range error')
			else:
				if (last_char == '\ '[0]) or (last_char == ', '[0]) or (last_char == '. '[0]) or (last_char == '( '[0]) or (last_char == ') '[0]):
					self.input_username.set(self.input_username.get()[:-1])

		self.input_username.trace("w", on_key_username)

		def on_key_password(*args):
			# Disable the use of '\' because it is reserved for commands
			try:
				last_char = self.input_password.get()[-1]
			except:
				pass
			else:
				if (last_char == '\ '[0]) or (last_char == ', '[0]) or (last_char == '. '[0]) or (last_char == '( '[0]) or (last_char == ') '[0]):
					self.input_password.set(self.input_password.get()[:-1])

		self.input_password.trace("w", on_key_password)

		username_entry.bind("<Return>", self.trylogin)
		password_entry.bind("<Return>", self.trylogin)

		button = Button(self, text="Log In", command = self.trylogin)
		button.grid(row=3, column=1)
		button = Button(self, text="Register", command = self.tryregister)
		button.grid(row=3, column=2)

		self.notifications = StringVar()
		self.notifications.set('')
		notifications_label = Label(self, textvariable=self.notifications)
		notifications_label.grid(row=4, columnspan=2)

	def trylogin(self, *args):
		if(self.input_password.get() and self.input_username.get()):
			self.controller.send_msg(r'\login='+self.input_username.get() + ','+self.input_password.get())

	def tryregister(self):
		if(self.input_password.get() and self.input_username.get()):
			self.controller.send_msg(r'\register='+self.input_username.get() + ','+self.input_password.get())

	def send_msg(self, msg):
		self.controller.output_lock.acquire()
		self.controller.output_queue.put(msg)
		self.controller.output_lock.release()

	def recv_msg(self, msg):
		if msg == r'\accept_login':
			self.controller.show_frame('ChatWindow')
		elif msg == r'\accept_register':
			#(to-do) register msg
			self.input_password.set('')
			self.notifications.set('Successfull registration')
		elif msg == r'\invalid_login_password':
			#(to-do) reject msg
			self.input_password.set('')
			self.notifications.set('Invalid Password')
		elif msg == r'\invalid_login_username':
			#(to-do) reject msg
			self.input_username.set('')
			self.input_password.set('')
			self.notifications.set('Invalid Username')
		elif msg == r'\invalid_register_username':
			#(to-do) reject msg
			self.input_username.set('')
			self.input_password.set('')
			self.notifications.set('This username is already taken')

def main():
	window = Tk()
	LoginWindow(window, None, None, None).pack(side=TOP, fill=BOTH, expand=True)

	window.geometry("400x400+300+300")
	window.mainloop()

if __name__ == "__main__":
	main()