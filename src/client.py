"""Client for communicating with echo server."""


import socket
import sys


def client(message, port):
    """Creates the protocol for interacting with server."""
    if len(message) % 8 == 0:
        message += '$'
    info = socket.getaddrinfo('127.0.0.1', port)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_socket = socket.socket(*stream_info[:3])
    client_socket.connect(stream_info[-1])
    buffer_length = 8
    response = ""
    print(message.encode('utf-8'))
    client_socket.sendall(message.encode('utf-8'))
    start_response = b""
    while b"\r\n\r\n" not in start_response:
        data = client_socket.recv(buffer_length)
        start_response += data
    stop_ind = start_response.index(b"\r\n\r\n") + 4
    response = start_response[:stop_ind].decode("utf-8")
    body = start_response[stop_ind:]
    while True:
        data = client_socket.recv(buffer_length)
        body += data
        if len(data) < buffer_length:
            break
    # if "Content-Type: .png" not in response and "Content-Type: .jpg" not in response:
    #     body = body.decode("utf-8")
    client_socket.close()
    print(response.encode('utf-8') + body)
    return response.encode("utf-8") + body
