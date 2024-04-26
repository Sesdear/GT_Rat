# -*- coding: utf-8 -*-

import socket
import threading
PORT: int = 1984
IP: str = ''

sock = socket.socket()
sock.bind((IP, 1984))
sock.listen(30)
Threads = []
Clients = [] #S ocket, address, UUID

SuThreads = []
SuClients = [] #S ocket, address, UUID



"""UTIL"""
def checkClientDuplicates(TupleList: list, hostname: str):
    for i in TupleList:
        if hostname in i:
            return True
    return False

def getSocketByHostname(list_of_tuples, search_string):
    for i in list_of_tuples:
        if search_string in i:
            return i[0]
    return None
def sendToClient(clientsocket: socket, command: str):
    clientsocket.send(bytes(command, encoding = 'utf-8'))

def sendToClientByName(comp_name: str, command: str, list_of_tuples: list):
    clientsocket = getSocketByHostname(list_of_tuples, comp_name)
    clientsocket.send(bytes(command, encoding = 'utf-8'))

def on_new_client(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        if msg == b"":
            clientsocket.close()
            return
        else:
            print(f"{msg}")
            return msg

        '''Some Handler Here'''

def clientListener(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        if msg == b"":
            clientsocket.close()
            return
        else:
            print(f"{msg}")
        '''Some Handler Here'''

def suClientListener(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        if msg == b"":
            clientsocket.close()
            return
        else:
            print(f"{msg}")
        '''Some Handler Here'''



try:
    while True:
        conn, addr = sock.accept()
        hostname = socket.gethostname()
        print(hostname, 'connected:', addr)

        msg = on_new_client(conn, addr)
        if msg == b"client":
            if not checkClientDuplicates(Clients, hostname):
                Clients.append((conn, addr, hostname))
                Threads.append(threading.Thread(target=clientListener, args = (conn, addr)))
                Threads[len(Threads)-1].start()
                for index, i in enumerate(Threads):
                    if not i.is_alive():
                        Threads.pop(index)
                        Clients.pop(index)
                print(Threads)
                print(Clients)
                sendToClientByName("DESKTOP-BO4V25B", "ABAS", Clients)
            else:
                print("DUPLICATE PC")
        elif msg == b"sudo":
            if not checkClientDuplicates(SuClients, hostname):
                SuClients.append((conn, addr, hostname))
                SuThreads.append(threading.Thread(target=suClientListener, args=(conn, addr)))
                SuThreads[len(SuThreads) - 1].start()
                for index, i in enumerate(Threads):
                    if not i.is_alive():
                        SuThreads.pop(index)
                        SuClients.pop(index)
                print(SuThreads)
                print(SuClients)
                sendToClientByName("DESKTOP-BO4V25B", "SUDO", SuClients)
            else:
                print("DUPLICATE SUDO PC")

except socket.error or socket.timeout as e:
    print("NUH UH")


