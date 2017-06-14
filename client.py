import socket, select, string, sys, queue

from threading import *
from tkinter import *

class ChatClient(Thread):
	def __init__(self, host, port):
		Thread.__init__(self)
		self.host = host
		self.port = int(port)
		self.output_queue = queue.Queue()

		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
			print('Failed to create socket')
			#(to-do) evaluate if it is correct to 'sys.exit()'
			sys.exit()

	def sendMsg(self, msg):
		data = bytes(msg, 'UTF-8')
		self.client_socket.send(data)

	def run(self):
		try :
			self.client_socket.connect((self.host, self.port))
		except socket.error:
			print('Unable to connect to (' + str(self.host) + ',' + str(self.port) + ')')
			return

		print('Connection successfull')

		#(to-do) evaluate if there is no better condition other than 'while 1'
		while 1:
			socket_list = [sys.stdin, self.client_socket]
			
			# Get the list sockets which are readable
			read_sockets, write_sockets, error_sockets = select.select(socket_list , [self.client_socket], [])
			
			for sock in read_sockets:

				if sock is self.client_socket:
					# Receive message from the server
					try:
						data = sock.recv(4096).decode('UTF-8')
					except socket.error:
						print('Could not reach server')
						sock.close()
						return

					if not data :
						# Received a blank message, therefore, the server is down
						print('Disconnected from server')
						sock.close()
						return
					else :
						# Valid message received

						# (to-do) Add msg to chat window here

						sys.stdout.write(data)				 
						sys.stdout.flush()
				else:
					# Send input from the user
					msg = sys.stdin.readline()

					if msg == '\n' :
						#(to-do) remove this and make a better logic for closing a connection
						sock.close()
						return
					else:
						self.output_queue.put(msg)

			for sock in write_sockets:
				while not self.output_queue.empty():
					msg = self.output_queue.get_nowait()
					sock.send(bytes(msg, 'UTF-8'))

#End of 'ChatClient' definition

def main():
	if(len(sys.argv) !=	 3) :
		print('Invalid number of arguments')
		sys.exit()

	client = ChatClient(sys.argv[1], sys.argv[2])
	client.run()

if __name__ == "__main__":
	main()