#!/bin/bash


import argparse
import socket
import threading
import time


class Server:
    '''
    Handles the creation and management of server connections.

    Attributes:
        client_connections (list): List that contains the active connections.
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

        print("[SERVER] Establishing server...")
        time.sleep(1)
        self.server_socket.listen(5)
        print(f"[SERVER] Established server on port {self.port}.")

    def run_server(self):
        '''
        Accepts client connections for established socket.
        '''
        while True:
            try:
                connection, address = self.server_socket.accept()
                print(f"Accepted connection from {address}")
                # begin thread for sending data
                connection_thread = threading.Thread(
                    target=self.data_handler, args=(connection, address))
                connection_thread.daemon = True
                connection_thread.start()
                # add connected client to list of clients
                self.client_connections.append(connection)
            except Exception as e:
                print(str(e))

    def data_handler(self, connection, address):
        '''
        Handles data flow from the connected client/s and broadcasts the message to 
        all connected clients.
        '''
        while True:
            data = connection.recv(1024).decode('utf-8')
            for connection in self.client_connections:
                connection.sendall(data.encode('utf-8'))
            if not data:
                print(f"{self.ip} from port: {self.port} has disconnected")
                self.client_connections.remove(connection)
                connection.close()
                break

    def stop_server(self):
        for connection in self.client_connections:
            self.client_connections.remove(connection)
            connection.close()


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
        port = int(options.port)
        print(options.port)
    except Exception:
        print("[SERVER] Which port would you like to communicate on? ")
        port = int(input(options.port))

    server_ip_name = socket.gethostname()
    server_ip = socket.gethostbyname(server_ip_name)
    print(f"The server's address to connect to is {server_ip}")

    server = Server(server_ip, port)

    try:
        server.establish_server()
        server.run_server()
    except KeyboardInterrupt:
        print("[SERVER] Closing server.")
        server.stop_server()
        server.server_socket.close()


if __name__ == "__main__":
    main()
