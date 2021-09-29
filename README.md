# ChatApp

1) Develop and describe an algorithmic solution for an application that utilises two way communication over a network (300 - 500 words)

2) Develop a flowchart for an application that outlines the control flow of the app, and illustrates the operation of an algorithm based on the solution you have described.

The Solution Must:
- describe how input and output will be handled
-detail how the solution will be structured in terms of classes, functions and other entities
- illustrate how the algorithm will function
- list the Python dependencies required and state what each will be used for (this includes Python standard libraries as well as third-party packages)

Provides a comprehensively detailed description of an application which utilises an algorithm for two way communication over a network including detail on input, output handling, structure, and dependencies with an accompanying flowchart that provides a comprehensive outline of the control flow of the application AND the operation of the algorithm


## Algorithmic Solution for ChatApp

• The application itself is a chat room app which offers different cipher options for users/clients to use when they send text or files over the socket network to the server. What they can send includes text messages / ascii art / photos / videos. The chat room itself is limited to 5 users. 

• The different cihpers will be encapsulated in their respective classes, along with the Diffie-Hellman key exchange as well. There will also be a section for client classes and server classes to handle connection to the server and client interaction between the clients via sockets and threading. These classes will then be called in main.py to facilitate running the application itself.

• As mentioned earlier, the application will utilize a cryptographic key exchange via the Diffie-Hellman key exchange method. This is to ensure that messages/files that are sent and received from client to client via the server are safely exchanged.

• Once the key exchange is complete and verified, the users are able to send messages/files via sockets and are able to chat inside the terminal window. 

• This application/solution will require a few dependencies, to facilitate communication between clients over a network they are as follows:

    • socket (any version above 3.5): This will be used for establishing a server for the chat room and handling the connection of users. 

    • threading (any version above 3.): Threading will be used to enable users to asynchronously message in the chat room.

    • random (any version above 3.): This module is used to randomly select the the random prime numbers to be used for key exchanges. 

    • argparse (version 3.2): This module is to be used to facilitate a user-friendly command-line interface when the user intiates either server.py or client.py.

   # • math (any version above 3.)