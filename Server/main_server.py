import socket
import threading
import FromSuClientCommandParser
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

def getHostnameBySocket(list_of_tuples, socket):
    for i in list_of_tuples:
        if socket in i:
            return i[2]
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
            str_reply = f"from {getHostnameBySocket(clientsocket, Clients)} : {msg}"
            for i in SuClients:
                sendToClient(i[0], str_reply)
        '''Some Handler Here'''

def suClientListener(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        if msg == b"":
            print("close(((")
            #deleteConnection(SuClients, SuThreads, clientsocket)
            clientsocket.close()
            return
        else:
            print(f"{msg}")
            data = FromSuClientCommandParser.parse(msg)
            print(data)
            if data[0] == "SERVER":
                pass
            else:
                if checkClientDuplicates(Clients, data[0]):
                    sendToClientByName(data[0], data[1], Clients)
                    print(f"sending {data[1]} to {data[0]}")
                    #sendToClient(clientsocket, f"sending {data[1]} to {data[0]}")
        '''Some Handler Here'''


def deleteConnection(ClientsList: list, ThreadsList: list, socket):
    index = ClientsList.index(socket)
    ClientsList.pop(index)
    ThreadsList.pop(index)

def updateConnectionsLists(ClientsList: list, ThreadsList: list):
    for index, i in enumerate(ThreadsList):
        if not i.is_alive():
            ThreadsList.pop(index)
            ClientsList.pop(index)
    for index, i in enumerate(ClientsList):
        if i.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) != 0:
            ThreadsList.pop(index)
            ClientsList.pop(index)

def serverTick():
    try:
        while True:
            conn, addr = sock.accept()
            hostname = socket.gethostname()
            print(hostname, 'connected:', addr)

            msg = on_new_client(conn, addr)
            if msg == b"client":
                updateConnectionsLists(Clients, Threads)
                if not checkClientDuplicates(Clients, hostname):
                    Clients.append((conn, addr, hostname))
                    Threads.append(threading.Thread(target=clientListener, args = (conn, addr)))
                    Threads[len(Threads)-1].start()
                    print(Threads)
                    print(Clients)
                    # sendToClientByName("DESKTOP-BO4V25B", "", Clients)
                else:
                    print("DUPLICATE PC")
            elif msg == b"sudo":
                updateConnectionsLists(SuClients, SuThreads)
                print(SuClients)
                if not checkClientDuplicates(SuClients, hostname):
                    SuClients.append((conn, addr, hostname))
                    SuThreads.append(threading.Thread(target=suClientListener, args=(conn, addr)))
                    SuThreads[len(SuThreads) - 1].start()
                    print(SuThreads)
                    print(SuClients)
                    sendToClient(conn, "SUDO USER ACTIVATED")
                else:
                    print("DUPLICATE SUDO PC")

    except socket.error or socket.timeout as e:
        print("NUH UH")


serverTick()
