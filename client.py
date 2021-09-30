#!/bin/bash

import socket
import threading
import sys
import argparse


class Client:
    '''
    Handles the management of client to server connections.

    Attributes: 
        server_ip (str): Represents the host IP address for the listening socket.
        server_port (int): The port number to used for the listening socket.
        username (str): The clients username for chat.
        client_socket (socket.socket): The client socket object for connection to server.
    '''

    def __init__(self, server_ip, server_port) -> None:
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = None
        self.client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def start_connection(self):
        '''
        Handles the client/s connection to server.
        '''
        try:
            print(
                f"Attempting to connect to {self.server_ip} on {self.server_port}\n")
            self.client_socket.connect((self.server_ip, self.server_port))
            print(
                f"Successfully connected to {self.server_ip} on {self.server_port}\n")
        except InterruptedError:
            print("Something went wrong, exiting.")
            sys.exit()

        # key exchange will happen here

        # might create a method for setting username (will need to write and read from json file)
        self.username = input("Please enter your username: \n")
        print(f"Hi {self.username}, welcome to the chat room!\n")
        print("You may now send messages to the room.")

        input_thread = threading.Thread(target=self.send_data)
        input_thread.daemon = True
        input_thread.start()

        # insert key methods here

        # might just turn into handler class for data
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            print(data)

    def send_data(self):
        while True:
            self.client_socket.send(bytes(input(''), 'utf-8'))


def main():
    '''
    Handles running the client script to connect to esablished server, setting 
    commad-line args and disconnection of client fro server.
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--server", dest="server_ip",
                        help="Server's IP to connect to.")
    parser.add_argument("-p", "--port", dest="server_port",
                        help="Server's PORT to connect to.")

    options = parser.parse_args()

    try:
        server_ip = options.server_ip
        port = int(options.server_port)
    except Exception:
        server_ip = input("Please enter server's IP here: ")
        port = int(input("Please enter server's PORT here: "))

    client = Client(server_ip, port)
    client.start_connection()
    client.send_data()


if __name__ == "__main__":
    main()
