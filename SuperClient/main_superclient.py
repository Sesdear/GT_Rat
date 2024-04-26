import random
import socket

PORT: int = 1984
IP: str = 'localhost'

sock = socket.socket()
sock.connect((IP, PORT))

def enteringMessage():
    message = "sudo"
    sock.send(bytes(message, encoding='utf-8'))

enteringMessage()

data = sock.recv(1024)
#sock.close()

print (data)
input()