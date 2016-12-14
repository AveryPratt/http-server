"""Server programmed to echo messages from client."""


import socket
import sys


def server():
    """Recieves a message from the client and echos it back."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ("127.0.0.1", 5003)
    server_socket.bind(address)
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    buffer_length = 8
    message_complete = False
    response = ""
    while not message_complete:
        if len(response) < buffer_length:
            if response == "":
                conn.sendall(response_error().encode('utf8'))
            break
        response += conn.recv(buffer_length).decode('utf8')
    conn.close()
    print(response)
    conn.sendall(response_ok().encode('utf8'))


def response_ok():
    """Returns 200 OK response"""
    response = ("HTTP/1.1 200 OK\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\n" +
        "Server: Teddy Bear\n" +
        "Last-Modified: Wed, 22 Jul 1884 19:15:56 GMT\n" +
        "Content-Length: 88\n" +
        "Content-Type: text/html\n" +
        "Connection: Closed\n" +
        "<html>\n" +
        "<body>\n" +
        "<h1>Hello, World!</h1>\n" +
        "</body>\n" +
        "</html>")
    return response

def response_error():
    """Returns 500 Internal Server Error response"""
    response = ("HTTP/1.1 500 Internal Server Error\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\n" +
        "Server: Teddy Bear\n" +
        "Last-Modified: Wed, 22 Jul 1884 19:15:56 GMT\n" +
        "Content-Length: 96\n" +
        "Content-Type: text/html\n" +
        "Connection: Closed\n" +
        "<html>\n" +
        "<body>\n" +
        "<h1>Internal Server Error</h1>\n" +
        "</body>\n" +
        "</html>")
    return response

server()
