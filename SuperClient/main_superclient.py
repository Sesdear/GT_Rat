import random
import socket
import sched
import time

PORT: int = 1984
IP: str = 'localhost'

sock = socket.socket()
connected = False

def connect():
    try:
        sock.connect((IP, PORT))
        enteringMessage()

        data = sock.recv(1024)
        print(data)
        global connected
        connected = True
        suClientTick()
    except socket.error as e:
        print(e)
def enteringMessage():
    message = "sudo"
    sock.send(bytes(message, encoding='utf-8'))

def sendMessage(message: str):
    sock.send(bytes(message, encoding='utf-8'))

def suConnectTick(): #NOT WORKING FUCK
    scheduler = sched.scheduler(time.time, time.sleep)
    global evt
    if not connected:
        evt = scheduler.enter(60, 1, connect)
        print("Reconnecting...")
    else:
        scheduler.cancel(evt)
        print("Connected!")
    scheduler.run()

def suClientTick():
    try:
        while True:
            msg = input(">>> ")
            if msg == "exit":
                sendMessage("")
                break
            sendMessage(msg)
            data = sock.recv(1024)
            print(data)
    except socket.error as e:
        print(e)

#suConnectTick()
connect()