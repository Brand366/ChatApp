#!/bin/bash

import socket
import threading
import sys
import argparse


class Client:
    '''
    Handles the management of client to server connections.

    Attributes: 
        ip (str): Represents the host IP address for the listening socket.
        port (int): The port number to used for the listening socket.
        username (str): The clients username for chat.
        client_socket (socket.socket): The client socket object for connection to server.
    '''

    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.username = None
        self.client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self):
        '''
        Handles the client/s connection to server.
        '''
        try:
            print(f"Attempting to connect to {self.ip} on {self.port}\n")
            self.client_socket.connect((self.ip, self.port))
            print(f"Successfully connected to {self.ip} on {self.port}\n")
        except InterruptedError:
            print("Something went wrong, exiting.")
            sys.exit()

        # key exchange will happen here

        # might create a method for setting username (will need to write and read from json file)
        self.username = input("Please enter your username: \n")
        print(f"Hi {self.username}, welcome to the chat room!\n")
        print("You may now send messages to the room.")

        input_thread = threading.Thread(target=self.send)
        input_thread.daemon = True
        input_thread.start()

        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            print(data)

    def send_data(self):
        while True:
            self.client_socket.send(bytes(input(''), 'utf-8'))
