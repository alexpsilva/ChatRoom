from chat_window import *
from login_window import *

class TopLevel(Tk):

	def __init__(self, output_q, output_l):
		Tk.__init__(self)
		self.output_queue = output_q
		self.output_lock = output_l

		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.top_frame = None
		self.frames = {}
		for F in (LoginWindow, ChatWindow):
			page_name = F.__name__
			frame = F(container, self)
			self.frames[page_name] = frame
			
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("LoginWindow")

		self.protocol("WM_DELETE_WINDOW", self.on_closing)

	def show_frame(self, page_name):
		self.top_frame = self.frames[page_name]
		self.top_frame.tkraise()

	def send_msg(self, msg):
		self.output_lock.acquire()
		self.output_queue.put(msg)
		self.output_lock.release()

	def recv_msg(self, msg):
		self.top_frame.recv_msg(msg)

	def on_closing(self):
		self.send_msg('')
		self.quit()

def main():
	window = TopLevel(None, None)
	window.geometry("400x400+300+300")
	window.mainloop()

if __name__ == "__main__":
	main()
