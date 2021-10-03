#!/bin/bash


import argparse
import socket
import time
import sys
import threading
from encryption import Vigenere


class Client:
    '''
    Handles the management of client to server connections.

    Attributes:
        ip (str): Represents the host IP address for the listening socket.
        port (int): The port number to used for the listening socket.
        username (str): The client's username for chat.
        key (str): The key used for the Vigenère Cipher.
        client_socket (socket.socket): The client socket object for connection to server.
    '''

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.username = None
        self.key = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.socket

    def connect_server(self):
        '''
        Handles the client/s connection to server and receiving data sent from server.
        '''
        try:
            print(
                f"Attempting to connect to {self.ip} on {self.port}")
            time.sleep(1)
            self.client_socket.connect((self.ip, self.port))
            print(
                f"Successfully connected to {self.ip} on {self.port}\n")
        except InterruptedError:
            print("Something went wrong, exiting.")
            sys.exit()
        except Exception as e:
            print(str(e))
            print("Oops, it seems the server is not running yet. Shutting down.")
            sys.exit()

        # client is able to set their username to help identify themself in the chat
        self.username = input("Please enter your username: ")
        print(f"Hi {self.username}, welcome to the chat room!\n")
        time.sleep(2)

        # thread for sending data to server begins here
        data_thread = threading.Thread(target=self.send_data)
        data_thread.daemon = True
        data_thread.start()

        # announces the client who joined to all connected clients
        self.client_socket.sendall(
            f'[SERVER] {self.username} has joined the room.\n'.encode('utf-8'))
        # bunch of client usage notifications for chat room
        print(
            "To leave the the chat room, type 'LEAVE' or input 'ctl+c' in the terminal.\n")
        print("To use the Vigenère Cipher, type 'VIGENERE'\n")
        print(
            "[WARNING] Any symbols and numbers used will be discarded with the cipher.\n")
        time.sleep(1)
        print("You may now send messages to the room.\n")

        # this is where data is received via the server
        while True:
            data = self.client_socket.recv(2048).decode('utf-8')
            if not data:
                # if server is closed, exits the client program
                print("Lost connection to the server.")
                print("The program will now shutdown.")
                self.client_socket.close()
                sys.exit()
            print(data)

    def send_data(self):
        '''
        Handles sending data to server, allows client to leave chat room and
        enables the client to use the Vigenère Cipher for messaging.
        '''
        while True:
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            if message == "VIGENERE":
                self.key = input(
                    "Please enter a key to use the Vigenère Cipher for the message: ")
                print("Now enter the text you would like encrypted.")

                sys.stdout.flush()
                message = sys.stdin.readline()[:-1]
                # dynamincally recreates the key and message
                cipher_obj = Vigenere(message, self.key)
                cipher_text = cipher_obj.encrypt()
                deciphered_text = cipher_obj.decrypt()

                self.client_socket.sendall(
                    f"{self.username} sent this cipher text: {cipher_text}".encode('utf-8'))
                cipher_input = input(
                    "[SERVER] Would you like to see the deciphered text? 'Y' for yes and 'N' for no. \n")

                if cipher_input == "Y":
                    self.client_socket.sendall(
                        f"{self.username}'s decipered text: {deciphered_text}".encode('utf-8'))
                    print("You may continue messaging :)")
                    continue
                elif cipher_input == "N":
                    print("You may continue messaging :)")
                    continue
            # allows the client to exit and notifys other connected client's
            elif message == "LEAVE":
                self.client_socket.sendall(
                    (f"{self.username} has the left the chat room.".encode('utf-8')))
                break

            else:
                self.client_socket.sendall(
                    f"{self.username}: {message}".encode('utf-8'))
        self.end_connection()

    def end_connection(self):
        '''
        Handles exiting the client program.
        '''
        print("Leaving chat room and closing connection...")
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
    except KeyboardInterrupt:
        client.end_connection()
    except Exception as e:
        print(
            "[Server] Error. Please see following message for information.", str(e))


if __name__ == "__main__":
    main()
