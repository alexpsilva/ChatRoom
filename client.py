import socket, select, string, sys, queue

from chat_client import *
from top_level import *

output_queue = queue.Queue()
output_lock = threading.Lock()

#root = TopLevel(output_queue, output_lock)
socket_thread = ChatClient(output_queue, output_lock)

gui = TopLevel(output_queue, output_lock, socket_thread)	

gui.geometry("400x410+300+200")
gui.mainloop()

socket_thread.join()

#(to-do) make a better logic to close the window and connection