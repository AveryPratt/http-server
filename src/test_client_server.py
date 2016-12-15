"""Tests to make sure client and server can communicate via sockets."""


import pytest


REQUESTS = [
    [
        "OK",
        ("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n")
    ],
    [
        "method",
        ("PUT /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n")
    ],
    [
        "version",
        ("GET /teddy/bear.html HTTP/1.0\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n")
    ],
    [
        "host",
        ("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n")
    ],
    [
        "format",
        ("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date : Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n")
    ],
]


REQUESTS_RESPONSES = [
    [
        "OK",
        ("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ("HTTP/1.1 200 OK\r\n" +
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
    ],
    [
        "method",
        ("PUT /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ("HTTP/1.1 405 Method Not Allowed\r\n" +
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
    ],
    [
        "version",
        ("GET /teddy/bear.html HTTP/1.0\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ("HTTP/1.1 403 Forbidden\r\n" +
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
    ],
    [
        "host",
        ("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n"),
        ("HTTP/1.1 417 Expectation Failed\r\n" +
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
    ],
    [
        "format",
        ("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date : Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ("HTTP/1.1 400 Bad Request\r\n" +
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
    ],
]

@pytest.mark.parametrize("status, request", REQUESTS)
def test_method_validation(status, request):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    import pdb; pdb.set_trace()
    from server import method_validation
    valid = method_validation(list(request))
    if status == "method":
        valid = not valid
    assert valid


@pytest.mark.parametrize("status, request", REQUESTS)
def test_version_validation(status, request):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    from server import version_validation
    valid = version_validation(list(request))
    if status == "version":
        valid = not valid
    assert valid


@pytest.mark.parametrize("status, request", REQUESTS)
def test_host_validation(status, request):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    from server import host_validation
    valid = host_validation(list(request))
    if status == "host":
        valid = not valid
    assert valid


@pytest.mark.parametrize("status, request", REQUESTS)
def test_format_validation(status, request):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    from server import format_validation
    valid = format_validation(list(request))
    if status == "format":
        valid = not valid
    assert valid

# uncomment below to run server tests

# def test_response_ok():
#     """Tests to see if valid client request will return a 200 OK message."""
#     from client import client
#     assert client("GET hello", 5007) == response


# def test_response_failed():
#     """Tests to see if invalid client request will return a 500 Error message"""
#     from client import client
#     assert client("fuck you.", 5008) == response
