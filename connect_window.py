from tkinter import *

class ConnectWindow(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.controller = controller

		self.input_host = StringVar()
		host_label = Label(self, text = "Hostname")
		host_label.grid(row=1, sticky=W)
		host_entry = Entry(self, text=self.input_host)
		host_entry.grid(row=1, column=1)

		self.input_port = StringVar()
		port_label = Label(self, text = "Port")
		port_label.grid(row=2, sticky=W)
		port_entry = Entry(self, text=self.input_port)
		port_entry.grid(row=2, column=1)

		def on_key_host(*args):
			# Disable the use of '\' because it is reserved for commands
			try:
				last_char = self.input_host.get()[-1]
			except:
				#(to-do) remove this
				print('Weird index out of range error')
			else:
				if (last_char == '\ '[0]) or (last_char == ', '[0]) or (last_char == '( '[0]) or (last_char == ') '[0]):
					self.input_host.set(self.input_host.get()[:-1])

		self.input_host.trace("w", on_key_host)

		def on_key_port(*args):
			# Disable the use of '\' because it is reserved for commands
			try:
				last_char = self.input_port.get()[-1]
			except:
				pass
			else:
				if (last_char == '0 '[0]) or (last_char == '1 '[0]) or (last_char == '2 '[0]) or (last_char == '3 '[0]) or (last_char == '4 '[0]) or (last_char == '5 '[0]) or (last_char == '6 '[0]) or (last_char == '7 '[0]) or (last_char == '8 '[0]) or (last_char == '9 '[0]):
					pass
				else:
					self.input_port.set(self.input_port.get()[:-1])

		self.input_port.trace("w", on_key_port)

		host_entry.bind("<Return>", self.tryconnect)
		port_entry.bind("<Return>", self.tryconnect)

		button = Button(self, text="Connect", command = self.tryconnect)
		button.grid(row=3)

		self.notifications = StringVar()
		self.notifications.set('')
		notifications_label = Label(self, textvariable=self.notifications)
		notifications_label.grid(row=4, columnspan=2)

	def tryconnect(self, *args):
		self.controller.connect(self.input_host.get(), self.input_port.get())

def main():
	window = Tk()
	ConnectWindow(window, None).pack(side=TOP, fill=BOTH, expand=True)

	window.geometry("400x400+300+300")
	window.mainloop()

if __name__ == "__main__":
	main()