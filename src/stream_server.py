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


import io


def server(socket, address):
    """Recieve a message from the client and sends a response back."""
    # server_socket = socket
    # server_socket.bind(address)
    # server_socket.listen(1)
    # conn, addr = server_socket.accept()
    buffer_length = 8
    req = buffer_request(buffer_length, socket)
    # print(req)
    socket.sendall(parse_request(req))
    socket.close()
    # conn.shutdown()


def buffer_request(buffer_length, socket):
    """Return a decoded client request."""
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
    """Return a server response based on client request formatting."""
    if not method_validation(request):
        return response_error("method")
    elif not version_validation(request):
        return response_error("version")
    elif not host_validation(request):
        return response_error("host")
    elif not format_validation(request):
        return response_error("format")
    try:
        print(request)
        uri = request.split(" ", 2)[1]
        info = resolve_uri(uri)
    except IOError:
        return response_error("404")
    return response_error("OK", info[0], info[1])


def method_validation(request):
    """Verify method formatting and type."""
    if request[0:4] != "GET ":
        return False
    return True


def version_validation(request):
    """Verify version formatting and type."""
    for ind in range(0, len(request)):
        if request[ind:ind + 9] == " HTTP/1.1":
            return True
    return False


def host_validation(request):
    """Verify host formatting and type."""
    for ind in range(0, len(request)):
        if request[ind:ind + 8] == "\r\nHost: ":
            return True
    return False


def format_validation(request):
    """Verify format formatting and type."""
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
    """Uri determines response body content."""
    import os
    root = 'webroot'
    uri = find_dir(root + uri)
    if os.path.isdir(uri):
        fials = os.listdir(uri)
        content_type = ".dir"
        center = "</li><li>".join(fials)
        body = "<html><body><ul><li>" + center + "</li></ul></body></html>"
    else:
        ind = uri.index(".")
        content_type = uri[ind:]
        if content_type == ".jpg" or content_type == ".png":
            fial = io.open(uri, "rb")
            body = str(fial.read())
        else:
            fial = io.open(uri, "r")
            body = fial.read()
        fial.close()
    return body, content_type


def response_error(key, body='', content_type=''):
    """Return the response for the error (or OK) specified by the key."""
    if content_type != ".jpg" and content_type != ".png":
        body = body.encode("utf-8")
    response_dict = {
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
        "404": ("HTTP/1.1 404 File Not Found\r\n" +
                    "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                    "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                    "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                    "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                    "Accept-Ranges:  none\r\n" +
                    "Content-Length: 438\r\n" +
                    "Connection: close\r\n" +
                    "Content-Type: text/html; charset=UTF-8\r\n" +
                    "\r\n" +
                    "<438 bytes of content>")
    }
    if content_type == ".png":
        content_type = 'image/png'
    elif content_type == ".jpg":
        content_type = 'image/jpeg'
    if key == "OK":
        response_dict[key] = ("HTTP/1.1 200 OK\r\n"
            "Date: Mon, 23 May 2005 22:38:34 GMT\r\n"
            "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n"
            "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n"
            "Etag: '3f80f-1b6-3e1cb03b'\r\n"
            "Accept-Ranges:  none\r\n"
            "Content-Length: " + str(len(body)) + "\r\n"
            "Connection: close\r\n"
            "Content-Type: " + content_type + "; charset=UTF-8\r\n"
            "\r\n" + body.decode('utf-8'))
    return response_dict[key] if key in response_dict else response_dict['format']


def find_dir(uri):
    """Find location of the uri on your system."""
    import os
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), uri)


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server_forever = StreamServer(('127.0.0.1', 10000), server)
    print('Starting teddy bear server on port 10000')
    server_forever.serve_forever()
