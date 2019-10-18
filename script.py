#!usr/bin/env python

import socket
import threading
import select
import time
import sys
from random import randint

class Server:
    connections = []
    peers =[] #if someone joins, everyone in the n/w must know that they've joined. Same if they leave.
    #??how are connections different from peers??
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP = "127.0.0.1" #can and should be changed later on
        port = 10000
        sock.bind((IP, port))
        #self.sock.listen(1)
        sock.listen(1)

        #the run function
        print("Server is running...")
        while True:
            #c, a= self.socket.accept()
            c, a= sock.accept()
            #a = tuple containing address of the port through which connections are incoming
            cThread = threading.Thread(target = self.handler, args = (c,a) )
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0]) #adding a peer when they connect
            print(str(a[0])+ ":" + str(a[1])+ " connected")
            self.sendPeers() #updating everyone when a new person joins the n/w

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not(data):
                print(str(a[0])+ ":" + str(a[1])+ " disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers() #updating everyone when a person leaves the n/w
                break

    def sendPeers(self):
        p =""
        for peer in self.peers:
            p = p + peer + ","

        for connection in self.connections:
            connection.send(b'\x11'+ bytes(p, "utf-8")) #we're sending the port of the peer in the form of bytes to the client



class Client:
    

    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, 10000))

        iThread = threading.Thread(target = self.sendMsg, args = (sock,))
        iThread.daemon = True
        iThread.start()

        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                print("got peers")
            else:
                print(str(data, "uft-8"))

if(len(sys.argv)>1):
    client = Client(sys.argv[1])

else:
    server = Server()


#while True:
    #print("Trying to connect...")
    #time.sleep(randint(1, 5))
