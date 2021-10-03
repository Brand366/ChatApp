#!/bin/bash


import argparse
import socket
import threading
import time
import sys


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
        # this is used to allow the same ip address to be used for server connection
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def establish_server(self):
        '''
        Creates and binds server socket and establishes listening socket for client connections.
        '''
        try:
            self.server_socket.bind((self.ip, self.port))
        except OSError as e:
            print(str(e))

        print("[SERVER] Establishing server...")
        time.sleep(1)
        self.server_socket.listen(10)
        print(f"[SERVER] Established server on port {self.port}.")
        print("[SERVER] To close the server and connected clients...")
        print("[SERVER] Simply input 'ctrl+c' in the command terminal.")

    def run_server(self):
        '''
        Accepts client connections for established socket.
        '''
        while True:
            try:
                c_connection, address = self.server_socket.accept()
                print(f"[SERVER] Accepted connection from {address}")
                # begin thread for sending data
                connection_thread = threading.Thread(
                    target=self.data_handler, args=(c_connection, address))
                connection_thread.daemon = True
                connection_thread.start()
                # add connected client to list of clients
                self.client_connections.append(c_connection)
            except Exception as e:
                print(str(e))

    def data_handler(self, c_connection, address):
        '''
        Handles data flow from the connected client/s and broadcasts the message to
        all connected clients.

        Args:
            connection (socket.socket): Connected client's socket.
            address (tuple): The socket address of the connected client.
        '''
        while True:
            data = c_connection.recv(2048).decode('utf-8')
            if data:
                print(f'{address} says {data}')
                self.broadcast_data(data, address)
            if not data:
                # if client disconnects, remove client from list and close relevant socket
                print(
                    f"[SERVER] {self.ip} from port: {self.port} has disconnected")
                self.client_connections.remove(c_connection)
                c_connection.close()
                return

    def send_data(self, c_connection,  data):
        '''
        Handles sending data to connected clients.

        Args:
            connection (socket.socket): Connected client's socket.
            data (str): The message that is to be sent.
        '''
        c_connection.sendall(data.encode('utf-8'))

    def broadcast_data(self, data, source):
        '''
        Handles broadcasting data to connected clients except for the source sender.

        Args:
            data (str): The message that is to be sent.
            source (tuple): The socket address of the source client.
        '''
        for connection in self.client_connections:
            if connection != source:
                self.send_data(connection, data)

    def stop_server(self):
        '''
        Handles closing all connected clients and ending the server conncetion.
        '''
        while len(self.client_connections) > 0:
            for connection in self.client_connections:
                self.client_connections.remove(connection)
                connection.close()
        print("[SERVER] Closing the server and disconnecting clients...")
        self.server_socket.close()


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
    except KeyboardInterrupt:
        sys.exit()

    server_ip_name = socket.gethostname()
    server_ip = socket.gethostbyname(server_ip_name)
    print(f"[SERVER] The server's address to connect to is {server_ip}")

    server = Server(server_ip, port)

    try:
        server.establish_server()
        server.run_server()
    except KeyboardInterrupt:
        server.stop_server()


if __name__ == "__main__":
    main()
