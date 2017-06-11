import socket, select, sys

if __name__ == '__main__':
	 
	if len(sys.argv) != 2:
		print('Invalid number of arguments')
		sys.exit()

	CONNECTION_LIST = []
	RECV_BUFFER = 4096
	port = int(sys.argv[1])

	try:
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as msg:
		print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
		sys.exit();

	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(('0.0.0.0', port))
	server_socket.listen(10)
 
	# Add server socket to the list of readable connections
	CONNECTION_LIST.append(server_socket)
 
	print('Chat server started on port ' + str(port))
 
	while 1:
		# Get the list sockets which are ready to be read through select
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
		for sock in read_sockets:
			if sock is server_socket:
				# New Connection
				new_socket, addr = server_socket.accept()
				new_socket.setblocking(0)
				CONNECTION_LIST.append(new_socket)
				print('Client (%s, %s) connected' % addr)

				#broadcast
				for send_socket in CONNECTION_LIST:
					if send_socket is not server_socket:
						try :
							send_socket.send(bytes('(%s, %s) entered the room' % addr, 'UTF-8'))
						except :
							# broken socket connection may be, chat client pressed ctrl+c for example
							send_socket.close()
							CONNECTION_LIST.remove(send_socket)
			 
			else:
				# Message sent from a client
				try:
					#In Windows, sometimes when a TCP program closes abruptly,
					# a 'Connection reset by peer' exception will be thrown
					data = sock.recv(RECV_BUFFER).decode('UTF-8')
					if data:
						#broadcast
						for send_socket in CONNECTION_LIST:
							if send_socket is not server_socket:
								try :
									send_socket.send(bytes('\r' + '<' + str(sock.getpeername()) + '> ' + data, 'UTF-8'))
								except :
									# broken socket connection may be, chat client pressed ctrl+c for example
									send_socket.close()
									CONNECTION_LIST.remove(send_socket)
				 
				except socket.error as msg:
					sock.close()
					CONNECTION_LIST.remove(sock)

					#broadcast
					for send_socket in CONNECTION_LIST:
						if send_socket is not server_socket:
							try :
								send_socket.send(bytes('Client (%s, %s) is offline' % addr, 'UTF-8'))
							except :
								# broken socket connection may be, chat client pressed ctrl+c for example
								send_socket.close()
								CONNECTION_LIST.remove(send_socket)

					continue
	 
	server_socket.close()