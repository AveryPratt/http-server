"""Tests to make sure client and server can communicate via sockets."""


import pytest


REQUESTS_RESPONSES = [
    [
        "OK",
        ("GET /teddy/bear.html HTTP/1.1 \r\n" +
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
        ("PUT /teddy/bear.html HTTP/1.1 \r\n" +
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
        ("GET /teddy/bear.html HTTP/1.0 \r\n" +
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
        ("GET /teddy/bear.html HTTP/1.1 \r\n" +
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
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
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


def test_response_ok():
    """Tests to see if valid client request will return a 200 OK message."""
    from client import client
    assert client("GET hello", 5007) == response


def test_response_failed():
    """Tests to see if invalid client request will return a 500 Error message"""
    from client import client
    assert client("fuck you.", 5008) == response
