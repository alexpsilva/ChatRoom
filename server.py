import socket, select, sys

class ChatServer():
	def __init__(self, port):
		self.port = port
		self.buffer_size = 4096
		self.connection_list = []

		try:
			self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print('Failed to create socket.')
			sys.exit();

		#(to-do) unsure about these configurations
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind(('0.0.0.0', port))
		self.server_socket.listen(10)

		self.connection_list.append(self.server_socket)
		print('Chat server started on port ' + str(port))

	def broadcast(self, msg):
		for send_socket in self.connection_list:
			if send_socket is not self.server_socket:
				try:
					send_socket.send(bytes(msg, 'UTF-8'))
				except socket.error:
					send_socket.close()
					self.connection_list.remove(send_socket)

	def run(self):
		while 1:
			# Get the list sockets which are ready to be read through select
			read_sockets,write_sockets,error_sockets = select.select(self.connection_list,[],[])
	 
			for sock in read_sockets:
				if sock is self.server_socket:
					# New Connection
					new_socket, addr = self.server_socket.accept()
					new_socket.setblocking(0)
					self.connection_list.append(new_socket)
					self.broadcast('(%s, %s) entered the room\n' % addr)			 
				else:
					# Message sent from a client
					try:
						data = sock.recv(self.buffer_size).decode('UTF-8')
						if data:
							self.broadcast('\r' + '<' + str(sock.getpeername()) + '> ' + data)
						else:
							sock.close()
							self.connection_list.remove(sock)
							self.broadcast('(%s, %s) has left the room\n' % addr)
					 
					except socket.error:
						sock.close()
						self.connection_list.remove(sock)
						self.broadcast('(%s, %s) has left the room\n' % addr)

		self.server_socket.close()

#End of 'ChatServer' definition

server = ChatServer(5000)
server.run()