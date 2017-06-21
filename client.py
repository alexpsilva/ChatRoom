import socket, select, string, sys, queue

from top_level import *

if(len(sys.argv) !=	 3) :
	print('Invalid number of arguments')
	sys.exit()

output_queue = queue.Queue()
output_lock = threading.Lock()

root = TopLevel(output_queue, output_lock)

class ChatClient(threading.Thread):
	def __init__(self, host, port, output_q, output_l):
		threading.Thread.__init__(self)
		self.host = host
		self.port = int(port)
		self.output_queue = output_q
		self.output_lock = output_l

		self._stop_event = threading.Event()

		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print('Failed to create socket')
			self.close()

	def stop(self):
		self.client_socket.close()
		root.quit()
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	def sendMsg(self, msg):
		data = bytes(msg, 'UTF-8')
		self.client_socket.send(data)

	def run(self):
		try :
			self.client_socket.connect((self.host, self.port))
		except socket.error:
			print('Unable to connect to (' + str(self.host) + ',' + str(self.port) + ')')
			self.stop()

		print('Connection successfull')

		#(to-do) evaluate if there is no better condition other than 'while 1'
		while 1:
			# Get the list sockets which are readable
			read_sockets, write_sockets, error_sockets = select.select([self.client_socket] , [self.client_socket], [])
			
			for sock in read_sockets:

				# Receive message from the server
				try:
					data = sock.recv(4096).decode('UTF-8')
				except socket.error:
					print('Could not reach server')
					sock.close()
					self.stop()

				if not data :
					# Received a blank message, therefore, the server is down
					print('Disconnected from server')
					sock.close()
					self.stop()
				else :
					# Valid message received

					global root
					root.recv_msg(data)						

			for sock in write_sockets:
				while not self.output_queue.empty():
					msg = self.output_queue.get_nowait()

					self.sendMsg(msg)
					if(msg == ''):
						self.stop()

#End of 'ChatClient' definition

socket_thread = ChatClient(sys.argv[1], sys.argv[2], output_queue, output_lock)
socket_thread.start()

root.geometry("400x410+300+200")
root.mainloop()

socket_thread.join()

#(to-do) make a better logic to close the window and connection