"""Server programmed to echo messages from client."""


import socket
import sys


def server():
    """Recieve a message from the client and echos it back."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ("127.0.0.1", 5005)
    server_socket.bind(address)
    server_socket.listen(3)
    conn, addr = server_socket.accept()
    buffer_length = 8
    message_complete = False
    response = ""
    while not message_complete:
        response += conn.recv(buffer_length).decode('utf8')
        if len(response) < buffer_length:
            break
    conn.sendall(response.encode('utf8'))
    conn.close()
    return response

if __name__ == '__main__':
    """Run server from command line."""
    server()
