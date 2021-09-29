#!/bin/bash

import socket
import threading
import argparse


class Server:
    '''
    Handles the creation and management of server connections.

    Attributes: 
        connections (list): List that contains the active connections.
        ip (str): Represents the host IP address for the listening socket.
        port (int): The port number to used for the listening socket.
        server_socket (socket.socket): The server socket object for connections from clients.
    '''

    def __init__(self, ip, port) -> None:
        self.client_connections = []
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def establish_server(self):
        '''
        Establishes listening server socket for client connections
        '''
        try:
            self.server_socket.bind((self.ip, self.port))
        except OSError as e:
            print(str(e))

        self.server_socket.listen(5)
        print(f"[SERVER] Establishing server on {self.ip} and {self.port}")

    def accept_connections(self):
        '''
        Accepts client connections for established socket.
        '''
        while True:
            # accept client connection
            c_c, c_a = self.server_socket.accept()
            print(f"[SERVER] Accepted a new connection from {c_a}")

            # client connection object here
            client_connect = ClientConnectionObj(
                self.client_socket, self.client_addr, encryp_key=None)

            # begin thread for client object
            connection_thread = threading.Thread(
                target=client_connect, args=(c_c, c_a))
            connection_thread.daemon = True
            connection_thread.start()

            # append threaded clients to list of clients
            self.client_connections.append(client_connect)

    def broadcast_data(self, data):
        '''
        Handles data to be sent to server and broadcasted to clients. :)
        '''

        for connection in self.client_connections:
            connection.send_data(data)

    # def stop_server(self):
    #     for connection in self.client_connections:
    #         connection.close()

    #     self.server_socket.close()


class ClientConnectionObj:
    '''
    Contains the client's information for server connection and supports receiving and sending data to server.
    '''

    def __init__(self, client_socket, client_addr, encryp_key) -> None:
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.encryp_key = encryp_key

        input_thread = threading.Thread(target=self.handler)
        input_thread.daemon = True
        input_thread.start()

    def handler(self):
        '''
        Manages the data flow from client to server & removes client connection.
        '''
        while True:
            data = self.client_socket.recv(1024).decode("utf-8")
            if data:
                print(f"{self.client_addr} sent: {data}")
            elif not data:
                print(
                    f"{self.client_socket} from {self.client_addr} has disconnected.")
                self.client_socket.close()
                Server.client_connections.remove(self.client_socket)
                break

    def send_data(self, data):
        '''
        Handles sending data from client to server.
        '''
        self.client_socket.sendall(data).encode("utf-8")


def main():
    '''
    Handles running the server script, organising the command-line args and
    closure of server plus connected clients.
    '''
    parser = argparse.ArgumentParser(description='ChatApp Server')
    parser.add_argument('ip', help='The IP address the server will run from.')
    parser.add_argument('-p', metavar='port', type=int, default=65432,
                        help='TCP port (default 65432)')

    options = parser.parse_args()

    try:
        options
        port = int(options.port)
    except Exception:
        port = int(input(options.port))

    server_ip_name = socket.gethostname()
    server_ip = socket.gethostbyname(server_ip_name)

    server = Server(server_ip, port)

    try:
        server.establish_server()
        server.accept_connections()
    except Exception as e:
        print("Something went wrong. Please see following message for information.", str(e))


if __name__ == "__main__":
    main()
