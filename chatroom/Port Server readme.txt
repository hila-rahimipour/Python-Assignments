Made by Matan Weinman
February 2022

ADDRESS: Depends on computer.
PORT: 55555

SERVER NAME REGEX: '[\w\d]+([\w\d\-_ ]+)?'

HOW TO USE:
1. Open a socket and connect to the server.

2. Send one of the following messages:
  - 'get': Used to get the IP and port of the server.
  - 'add': Used to add a server IP and port to the database.
  - 'del': Used to delete an existing query in the server.

3. 'GET' INSTRUCTIONS:
    Send the name of the server you want to connect to.
    If the name is found in the server, You will receive a string representation of a tuple, which can be processed using 'eval()'.
    If the name doesn't exist in the server, you will get the response 'no'.
    If the name is not in the correct format, you will receive the message 'format'.

4. 'ADD' INSTRUCTIONS:
    Send the following data in the following format: SERVER_NAME:IP:PORT
    If the name is already in use: You will receive 'used'.
    If the data is not in the correct format: You will receive 'no'.
    If successful: You will receive 'ok'.

5. 'DEL' INSTRUCTIONS:
    Send the server name.
    If the name doesn't exist, you will receive the message 'no'.
    If it does, you will receive 'ok', and your server data will be deleted from the port server.
    If the name is not in the correct format, you will receive 'format'.

To shut down the server, press 'Enter'. (Does NOT work only on IDLE. To disable it, change the boolean parameter 'enter_shutdown' to FALSE.)
When 'enter_shutdown' is True and the server has initiated shutdown, the server will wait for all ongoing communications to end. However, it will not accept new connections.
In addition, the server data will be saved to the file 'port_data.txt'. You can also read the file at the beginning, by changing the boolean parameter 'read_from_file'.