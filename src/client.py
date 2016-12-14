"""Client for communicating with echo server."""


import socket
import sys


def client(message):
    """Creates the protocol for interacting with server."""
    if len(message) % 8 == 0:
        message += '$'
    info = socket.getaddrinfo('127.0.0.1', 5119)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_socket = socket.socket(*stream_info[:3])
    client_socket.connect(stream_info[-1])
    buffer_length = 8
    reply_complete = False
    response = ""
    print(message.encode('utf-8'))
    client_socket.sendall(message.encode('utf-8'))
    while not reply_complete:
        data = client_socket.recv(buffer_length).decode('utf-8')
        response += data
        if len(data) < buffer_length:
            break
    client_socket.close()
    return response
