"""Server programmed to echo messages from client."""


import socket
import sys
import io

def server(port):
    """Recieves a message from the client and echos it back."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ("127.0.0.1", port)
    server_socket.bind(address)
    server_socket.listen(1)
    conn, addr = server_socket.accept()
    buffer_length = 8
    req = buffer_request(buffer_length, conn)
    print(req)
    conn.sendall(parse_request(req).encode('utf-8'))
    # conn.shutdown()
    conn.close()

def buffer_request(buffer_length, conn):
    req = ""
    while True:
        addition = conn.recv(buffer_length).decode('utf-8')
        req += addition
        if addition == "$":
            addition = ""
        if len(addition) < buffer_length:
            break
    return req

def parse_request(request):
    if not method_validation(request):
        return response_error("method")
    elif not version_validation(request):
        return response_error("version")
    elif not host_validation(request):
        return response_error("host")
    elif not format_validation(request):
        return response_error("format")
    uri = request.split(" ", 2)[1]
    info = resolve_uri(uri)
    return response_error("OK", info[0], info[1])


def method_validation(request):
    if request[0:4] != "GET ":
        return False
    return True

def version_validation(request):
    for ind in range(0, len(request)):
        if request[ind:ind + 9] == " HTTP/1.1":
            return True
    return False


def host_validation(request):
    for ind in range(0, len(request)):
        if request[ind:ind + 8] == "\r\nHost: ":
            return True
    return False

def format_validation(request):
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



def response_error(key, body=None, content_type=None):
    """Returns a response for an error (or OK) specified by the key."""
    response_dict = {
        "OK": ("HTTP/1.1 200 OK\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: " + str(len(body)) + "\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: " + content_type + "\r\n" +
                    "\r\n" + body),
        "method": ("HTTP/1.1 405 Method Not Allowed\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: 438\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    "\r\n" +
                    "<438 bytes of content>"),
        "version": ("HTTP/1.1 403 Forbidden\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: 438\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    "\r\n" +
                    "<438 bytes of content>"),
        "host": ("HTTP/1.1 417 Expectation Failed\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: 438\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    "\r\n" +
                    "<438 bytes of content>"),
        "format": ("HTTP/1.1 400 Bad Request\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: 438\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    "\r\n" +
                    "<438 bytes of content>"),
    }
    for each in response_dict:
        if key == each:
            return response_dict[key]
    return response_dict["format"]
