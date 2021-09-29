#!/bin/bash
import socket
import threading
import sys

'''
Simplified Version of ChatApp 
'''


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connections = []

    def __init__(self) -> None:
        self.sock.bind(('127.0.1.1', 10000))
        self.sock.listen(5)
        print("Listening for connections at port 10000")

    def handler(self, c_c, c_a):
        while True:
            data = c_c.recv(1024)
            for connection in self.client_connections:
                connection.send(data)
            if not data:
                print(repr(c_a[0]) + ':' + repr(c_a[1]), 'disconnected')
                self.client_connections.remove(connection)
                connection.close()
                break

    def run(self):
        while True:
            c_c, c_a = self.sock.accept()
            connection_thread = threading.Thread(
                target=self.handler, args=(c_c, c_a))
            connection_thread.daemon = True
            connection_thread.start()
            self.client_connections.append(c_c)
            print(repr(c_a[0]) + ':' + repr(c_a[1]), 'connected')


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self):
        while True:
            self.sock.send(bytes(input(''), 'utf-8'))

    def __init__(self, address) -> None:
        self.sock.connect((address, 10000))

        input_thread = threading.Thread(target=self.send)
        input_thread.daemon = True
        input_thread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(data)


if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()
