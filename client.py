#!/bin/bash


import argparse
import socket
import time
import sys
import threading


class Client:
    '''
    Handles the management of client to server connections.

    Attributes:
        ip (str): Represents the host IP address for the listening socket.
        port (int): The port number to used for the listening socket.
        username (str): The clients username for chat.
        client_socket (socket.socket): The client socket object for connection to server.
    '''

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.username = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.socket

    def connect_server(self):
        '''
        Handles the client/s connection to server.
        '''
        try:
            print(
                f"Attempting to connect to {self.ip} on {self.port}\n")
            time.sleep(1)
            self.client_socket.connect((self.ip, self.port))
            print(
                f"Successfully connected to {self.ip} on {self.port}\n")
        except InterruptedError:
            print("Something went wrong, exiting.")
            sys.exit()

        self.username = input("Please enter your username: ")
        print(f"Hi {self.username}, welcome to the chat room!\n")
        print("You may now send messages to the room.")
        print("To leave the the chat room, type 'LEAVE'")
        time.sleep(1)

        data_thread = threading.Thread(target=self.send_data)
        data_thread.daemon = True
        data_thread.start()

        self.client_socket.sendall(
            f'[SERVER] {self.username} has joined the room.'.encode('utf-8'))

        while True:
            data = self.client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(data)

    def send_data(self):
        while True:
            print(f"{self.username}", end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            if message == "LEAVE":
                self.client_socket.sendall(
                    (f"{self.username} has the left the chat room.".encode('utf-8')))
                break
            else:
                self.client_socket.sendall(
                    (f"{self.username}: {message}".encode('utf-8')))
        print("Leaving chat room...")
        self.client_socket.close()
        sys.exit()


def main():
    '''
    Handles running the client script to connect to esablished server, setting
    commad-line args and disconnection of client from server.
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--server", dest="ip",
                        help="Server's IP to connect to.")
    parser.add_argument("-p", "--port", dest="port",
                        help="Server's PORT to connect to.")

    options = parser.parse_args()

    try:
        server_ip = options.ip
        port = int(options.port)
    except Exception:
        server_ip = input("Please enter server's IP here: ")
        port = int(input("Please enter server's PORT here: "))

    client = Client(server_ip, port)

    try:
        client.connect_server()
        client.send_data()
    except OSError:
        client.client_socket.close()
    except Exception as e:
        print(
            "[Server] Error. Please see following message for information.", str(e))


if __name__ == "__main__":
    main()
