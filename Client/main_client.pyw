import random
import socket

PORT: int = 1984
IP: str = 'localhost'

sock = socket.socket()
sock.connect((IP, PORT))
message = "GOYDA"
if random.randint(1, 2) == 1:
    message = "CLIENT 1"
else:
    message = "CLIENT 2"
sock.send(bytes(message, encoding='utf-8'))

data = sock.recv(1024)
#sock.close()

print (data)
input()