import socket, select, sys, queue

class ChatServer():
	def __init__(self, port):
		self.port = port
		self.buffer_size = 4096

		try:
			self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print('Failed to create socket.')
			sys.exit();

		#(to-do) unsure about these configurations
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind(('localhost', port))
		self.server_socket.listen(10)

		self.inputs = [self.server_socket]
		self.outputs = []

		self.message_queues = {}
		self.usernames = {}

		print('Chat server started on port ' + str(port))

	def broadcast(self, msg):
		#(to-do) remove this print
		print(msg)
		for send_socket in self.inputs:
			if send_socket is not self.server_socket:
				self.message_queues[send_socket].put(msg)

				if send_socket not in self.outputs:
					self.outputs.append(send_socket)

	def remove(self, sock):
		if sock in self.outputs:
			self.outputs.remove(sock)
		self.inputs.remove(sock)
		sock.shutdown(socket.SHUT_RDWR)
		sock.close()

		del self.message_queues[sock]
		del self.usernames[sock]

	def run(self):
		while 1:
			# Get the list sockets which are ready to be read through select
			read_sockets,write_sockets,error_sockets = select.select(self.inputs, self.outputs, self.inputs)

			for sock in read_sockets:
				if sock is self.server_socket:
					# New Connection
					new_socket, new_addr = self.server_socket.accept()
					new_socket.setblocking(0)

					self.inputs.append(new_socket)
					self.message_queues[new_socket] = queue.Queue()
					self.usernames[new_socket] = str(new_addr)

					self.broadcast('<' + self.usernames[new_socket] + '> entered the room')			 
				else:
					# Message sent from a client
					try:
						data = sock.recv(self.buffer_size).decode('UTF-8')					 
					except socket.error:
						sock_addr = str(sock.getpeername())
						self.broadcast('<' + self.usernames[sock] + '> ' + 'has left the room')
						self.remove(sock)
					else:
						if data:
							# Valid message received from the client
							if r'\username=' in data:
								# Set this client's username to whatever is after '\username=' in the message
								self.usernames[sock] = data[10:] 
							else:
								self.broadcast('<' + self.usernames[sock] + '> ' + data)
						else:
							# Received a blank message, therefore, the client has closed the socket
							sock_addr = str(sock.getpeername())
							self.broadcast('<' + self.usernames[sock] + '> ' + 'has left the room')
							self.remove(sock)

			for sock in write_sockets:
				while not self.message_queues[sock].empty():
					msg = self.message_queues[sock].get_nowait()
					sock.send(bytes(msg, 'UTF-8'))
				self.outputs.remove(sock)

			for sock in error_sockets:
				sock_addr = str(sock.getpeername())
				self.broadcast('<' + self.usernames[sock] + '> ' + 'has left the room')
				self.remove(sock)

#End of 'ChatServer' definition

def main():
	server = ChatServer(5000)
	server.run()

if __name__ == "__main__":
	main()