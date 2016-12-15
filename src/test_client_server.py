"""Tests to make sure client and server can communicate via sockets."""


import pytest


def test_response_ok():
    """Tests to see if valid client request will return a 200 OK message."""
    from client import client
    response = ("HTTP/1.1 200 OK\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Last-Modified: Wed, 22 Jul 1884 19:15:56 GMT\r\n" +
        "Content-Length: 88\r\n" +
        "Content-Type: text/html\r\n" +
        "Connection: Closed\r\n\r\n" +
        "<html>\r\n" +
        "<body>\r\n" +
        "<h1>Hello, World!</h1>\r\n" +
        "</body>\r\n" +
        "</html>")
    assert client("GET hello", 5007) == response


def test_response_failed():
    """Tests to see if invalid client request will return a 500 Error message"""
    from client import client
    response = ("HTTP/1.1 500 Internal Server Error\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Last-Modified: Wed, 22 Jul 1884 19:15:56 GMT\r\n" +
        "Content-Length: 96\r\n" +
        "Content-Type: text/html\r\n" +
        "Connection: Closed\r\n\r\n" +
        "<html>\r\n" +
        "<body>\r\n" +
        "<h1>Internal Server Error</h1>\r\n" +
        "</body>\r\n" +
        "</html>")
    assert client("fuck you.", 5008) == response
