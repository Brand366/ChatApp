# ChatApp

This is a chatroom messaging application with a simple and optional Vigenère encryption.
This application also allows for multiple clients to connect to the server.

## How to Run:

First, run the `server.py` file from the command line.

The usage: `python3 server.py -p [PORT]`

Arguments: 
- `-p [PORT]`: The TCP port the server listens from (the default is 65432)

Example usage:

```
$ python3 server.py -p 65432
[SERVER] The server's address to connect to is 127.0.1.1
[SERVER] Establishing server...
[SERVER] Established server on port 65432.
```

```
$ python3 server.py [Enter whichever port]
[SERVER] The server's address to connect to is 127.0.1.1
[SERVER] Establishing server...
[SERVER] Established server on port 65432.
```

Run the `client.py` script from the command-line in a seperate terminal window.

The usage: `python3 client.py -ip [HOST] -p [PORT]`

Arguments:

- `-ip [HOST]`: The interface the server listens from. Can either be the IP address or host name.
- `-p [PORT]`: The TCP port the server has been established from.

Example usage:

```
$ python3 client.py -ip 127.0.1.1 -p 65432
Attempting to connect to 127.0.1.1 on 65432 
Successfully connected to 127.0.1.1 on 65432

Please enter your username:
```
