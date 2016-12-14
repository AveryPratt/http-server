"""Tests to make sure client and server can communicate via sockets."""


import pytest


def test_response_ok():
    """Tests to see if valid client request will return a 200 OK message."""
    from client import client
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
    assert client("hello") == response


def test_response_failed():
    """Tests to see if invalid client request will return a 500 Error message"""
    from client import client
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
    assert client(None) == response


# def test1():
#     """Test if string that is shorter than buffer length gets sent."""
#     assert client.client("hello") == "hello"


# def test2():
#     """Test if string that is longer than buffer length gets sent."""
#     assert client.client("I don't know why you say 'goodbye' I say 'hello'") == "I don't know why you say 'goodbye' I say 'hello'"


# def test3():
#     """Test if string that is longer than buffer length gets sent."""
#     assert client.client("hlo gdby") == "hlo gdby"


# def test4():
#     """Test if string that is longer than buffer length gets sent."""
#     assert client.client("¡¢£¤¥") == "¡¢£¤¥"
