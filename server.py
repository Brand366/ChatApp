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
            c_conn, c_addr = self.server_socket.accept()
            print(f"[SERVER] Accepted a new connection from {c_addr}")

            # client connection object here
            client_connect = ClientConnectionObj(
                self.c_conn, self.c_addr, encryp_key=None)

            # begin thread for client object
            connection_thread = threading.Thread(
                target=client_connect, args=(c_conn, c_addr))
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


class ClientConnectionObj:
    '''
    Contains the client's information for server connection and supports receiving and sending data to server.
    '''

    def __init__(self, c_conn, c_addr, encryp_key) -> None:
        self.c_conn = c_conn
        self.c_addr = c_addr
        self.encryp_key = encryp_key
        # not sure where to put the keys for DH and encryption...

        input_thread = threading.Thread(target=self.handler)
        input_thread.daemon = True
        input_thread.start()

    def handler(self):
        '''
        Manages the data flow from client to server & removes client connection.
        '''
        while True:
            data = self.c_conn.recv(1024).decode("utf-8")
            if data:
                print(f"{self.c_addr} sent: {data}")
            elif not data:
                print(
                    f"{self.c_conn} from {self.c_addr} has disconnected.")
                self.c_conn.close()
                Server.client_connections.remove(self.c_conn)
                break

    def send_data(self, data):
        '''
        Handles sending data from client to server.
        '''
        self.c_conn.sendall(data).encode("utf-8")


def main():
    '''
    Handles running the server script, organising the command-line args and
    closure of server plus connected clients.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, dest="port",
                        help="Port number for server to establish on.")
    options = parser.parse_args()

    try:
        options
        port = int(options.port)
    except Exception:
        print("Which port would you like to communicate on?")
        port = int(input(options.port))

    server_ip_name = socket.gethostname()
    server_ip = socket.gethostbyname(server_ip_name)
    print(f"The server's name to connect to is {server_ip_name}")

    server = Server(server_ip, port)

    try:
        server.establish_server()
        server.accept_connections()

    except KeyboardInterrupt:
        print("[SERVER] Closing server.")
        for connection in Server.client_connections:
            connection.c_conn.close()

        Server.server_socket.close()
    except Exception as e:
        print(
            "[Server] Error. Please see following message for information.", str(e))


if __name__ == "__main__":
    main()
