import socket, select, string, sys
 
def prompt() :
	sys.stdout.write('<You> ')
	sys.stdout.flush()

class ChatClient():
	def __init__(self, host, port):
		self.host = host
		self.port = int(port)

		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as msg:
			print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
			#(to-do) evaluate if it is correct to 'sys.exit()'
			sys.exit()

	def run(self):
		try :
			self.client_socket.connect((self.host, self.port))
		except socket.error as msg:
			print('Unable to connect to (' + str(self.host) + ',' + str(self.port) + ')')
			print(msg)
			#(to-do) evaluate if it is correct to 'sys.exit()'
			sys.exit()

		print('Connection successfull')
		prompt();

		#(to-do) evaluate if there is no better condition other than 'while 1'
		while 1:
			socket_list = [sys.stdin, self.client_socket]
			
			# Get the list sockets which are readable
			read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
			
			for sock in read_sockets:

				if sock is self.client_socket:
					# Receive message from the server
					data = sock.recv(4096).decode('UTF-8')

					if not data :
						print('\nDisconnected from server')
						#(to-do) evaluate if it is correct to 'sys.exit()'
						sys.exit()
					else :
						# Valid message received
						sys.stdout.write(data)
						prompt()
				 
				else:
					# Receive send input from the user
					data = bytes(sys.stdin.readline(), 'UTF-8')
					self.client_socket.send(data)
					prompt()

#End of 'ChatClient' definition


if(len(sys.argv) !=	 3) :
	print('Invalid number of arguments')
	sys.exit()

client = ChatClient(sys.argv[1], sys.argv[2])
client.run()