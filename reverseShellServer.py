#!/usr/bin/python

import socket

def getCommand(commandNum):
    if commandNum == '1':
        return b'1'
    if commandNum == '2':
        return b'2'
    
HOST = '0.0.0.0'
PORT = 3232

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

server_socket.listen(5)
print("Listening on port " + str(PORT) + ", waiting for connection")

client_socket, (client_ip, client_port) = server_socket.accept()

print("client " + client_ip + " connected")

while True:
    try:
        command = input(client_ip + ">")
        if(len(command.split()) != 0):
            print(command)
            print("after convert")
            #command = getCommand(command)
            #print(command)
            client_socket.send(str.encode(command))
            #client_socket.send(str.encode(command))
            #client_socket.send(command)
        else:
           continue
    except(EOFError):
           print("Invalid input")
           continue

    if(command == "quit"):
        break

    data = client_socket.recv(1024)
    print(data)

client_socket.close()