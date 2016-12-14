"""Client for communicating with echo server."""


import socket
import sys


def client(message):
    """Creates the protocol for interacting with server."""
    info = socket.getaddrinfo('127.0.0.1', 5003)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_socket = socket.socket(*stream_info[:3])
    client_socket.connect(stream_info[-1])
    buffer_length = 8
    reply_complete = False
    response = ""
    client_socket.sendall(message.encode('utf8'))
    # client_socket.listen(3)
    while not reply_complete:
        data = client_socket.recv(buffer_length).decode('utf8')
        response += data
        if len(response) < buffer_length:
            break
    client_socket.close()
    return response
