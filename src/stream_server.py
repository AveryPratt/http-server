"""Recieves a message from the client and sends back one of the
following responses with headers and a message body if the clients
request is valid:

200 OK: The client sends a valid request with a URI that exists.
405 Method Not Allowed: The client does not send a GET request.
403 Forbidden: The client sends a request with the wrong HTTP protocol.
417 Expectation Failed: The client sends a request with a bad host.
400 Bad Request: The client sends a request in an improper format.
404 File Not Found: THe client sends a request for a file that does not exist.
"""


import socket
import io


def server(socket, address):
    """Sets up a socket bound to an address and a port.
    Listens for and accepts incoming client connections.
    Processes client requests, builds an appropriate response,
    and sends that response back to the client."""
    # server_socket = socket
    # server_socket.bind(address)
    # server_socket.listen(1)
    # conn, addr = server_socket.accept()
    buffer_length = 8
    req = buffer_request(buffer_length, socket)
    # print(req)
    socket.sendall(parse_request(req).encode('utf-8'))
    socket.close()
    # conn.shutdown()


def buffer_request(buffer_length, socket):
    """Recieves client requests. Returns a string of 
    the client request plus a dollar sign.Removes a stray 
    dollar sign from client messages evenly
    divisible by eight."""
    req = ""
    while True:
        addition = socket.recv(buffer_length).decode('utf-8')
        req += addition
        if addition == "$":
            addition = ""
        if len(addition) < buffer_length:
            break
    return req


def parse_request(request):
    """Takes the client's request as a parameter.
    Returns the appropriate resopnse."""
    if not method_validation(request):
        return response_error("method")
    elif not version_validation(request):
        return response_error("version")
    elif not host_validation(request):
        return response_error("host")
    elif not format_validation(request):
        return response_error("format")
    try:
        uri = request.split(" ", 2)[1]
        info = resolve_uri(uri)
    except IOError:
        return response_error("404")
    return response_error("OK", info[0], info[1])


def method_validation(request):
    """"""
    if request[0:4] != "GET ":
        return False
    return True


def version_validation(request):
    """Docstring"""
    for ind in range(0, len(request)):
        if request[ind:ind + 9] == " HTTP/1.1":
            return True
    return False


def host_validation(request):
    """Docstring"""
    for ind in range(0, len(request)):
        if request[ind:ind + 8] == "\r\nHost: ":
            return True
    return False


def format_validation(request):
    """Docstring"""
    val_count = 0
    for ind in range(0, len(request)):
        if val_count == 0 or val_count == 1:
            if request[ind] == " ":
                val_count += 1
            elif request[ind:ind + 1] == "\r\n":
                return False
        elif val_count == 2:
            if request[ind:ind + 2] == "\r\n":
                val_count += 1
            elif request[ind] == " ":
                return False
        elif val_count % 2 == 1:
            if request[ind] == ":":
                val_count += 1
            elif request[ind] == " ":
                return False
        else:
            if request[ind] == "\r\n":
                val_count += 1
    return True


def resolve_uri(uri):
    """Docstring"""
    import io
    import os
    if "." not in uri:
        content_type = ".dir"
        fials = os.listdir(uri)
        center = "</li><li>".join(fials)
        body = "<html><body><ul><li>" + center + "</li></ul></body></html>"
    else:
        ind = uri.index(".")
        content_type = uri[ind:]
        if content_type == ".jpg" or content_type == ".png":
            fial = io.open(uri, "rb")
        else:
            fial = io.open(uri, "r")
        body = fial.read()
    return body, content_type


def response_error(key, body='', content_type=''):
    """Returns the response for the error (or OK) specified by the key."""
    response_dict = {
        "OK": (("HTTP/1.1 200 OK\r\n" +
                "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                "Accept-Ranges:  none\r\n" +
                "Content-Length: " + str(len(body)) + "\r\n" +
                "Connection: close\r\n" +
                "Content-Type: " + content_type + "\r\n" +
                "\r\n"), body),
        "method": (("HTTP/1.1 405 Method Not Allowed\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: 438\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    "\r\n"), "<438 bytes of content>"),
        "version": (("HTTP/1.1 403 Forbidden\r\n" +
                     "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                     "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                     "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                     "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                     "Accept-Ranges:  none\r\n" +
                     "Content-Length: 438\r\n" +
                     "Connection: close\r\n" +
                     "Content-Type: text/html; charset=UTF-8\r\n" +
                     "\r\n"), "<438 bytes of content>"),
        "host": (("HTTP/1.1 417 Expectation Failed\r\n" +
                  "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                  "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                  "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                  "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                  "Accept-Ranges:  none\r\n" +
                  "Content-Length: 438\r\n" +
                  "Connection: close\r\n" +
                  "Content-Type: text/html; charset=UTF-8\r\n" +
                  "\r\n"), "<438 bytes of content>"),
        "format": (("HTTP/1.1 400 Bad Request\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: 438\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    "\r\n"), "<438 bytes of content>"),
        "404": (("HTTP/1.1 404 File Not Found\r\n" +
                 "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                 "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                 "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                 "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                 "Accept-Ranges:  none\r\n" +
                 "Content-Length: 438\r\n" +
                 "Connection: close\r\n" +
                 "Content-Type: text/html; charset=UTF-8\r\n" +
                 "\r\n"), "<438 bytes of content>"),
    }
    for each in response_dict:
        if key == each:
            return response_dict[key]
    return response_dict["format"]
