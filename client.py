import socket, select, string, sys

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
if __name__ == "__main__":
     
    if(len(sys.argv) !=	 3) :
        print('Invalid number of arguments')
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    try:
    	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
	    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
	    sys.exit()

    client_socket.settimeout(2)
     
    try :
        client_socket.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
     
    print('Connected to remote host. Start sending messages')
    prompt()
     
    while 1:
        socket_list = [sys.stdin, client_socket]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            if sock is client_socket:
            	# Receive message from the server
                data = sock.recv(4096).decode('UTF-8')

                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    prompt()
             
            else :
            	# Receive message from the user
                data = bytes(sys.stdin.readline(), 'UTF-8')
                client_socket.send(data)
                prompt()