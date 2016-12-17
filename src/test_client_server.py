"""Tests to make sure client and server can communicate via sockets."""


import pytest
import io


jpg_file_text = io.open('webroot/images/Sample_Scene_Balls.jpg', 'rb')
jpg_file_read = jpg_file_text.read()
png_file_text = io.open('webroot/images/sample_1.png', 'rb')
png_file_read = png_file_text.read()


GOOD_REQUESTS = [
    [
        ".dir",
        ("GET webroot HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ("<html><body><ul><li>a_web_page.html</li><li>images</li><li>make_time.py</li>" +
        "<li>sample.txt</li></ul></body></html>")
    ],
    [
        ".html",
        ("GET webroot/a_web_page.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ("<!DOCTYPE html>\n<html>\n<body>\n\n<h1>Code Fellows</h1>\n\n<p>" +
        "A fine place to learn Python web programming!</p>\n\n</body>\n</html>")
    ],
    [
        ".py",
        ("GET webroot/make_time.py HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ('#!/usr/bin/env python\n\n"""\nmake_time.py\n\nsimple script that returns and HTML page' +
        ' with the current time\n"""\n\nimport datetime\n\ntime_str = ' +
        'datetime.datetime.now().isoformat()\n\nhtml = """\n<http>\n<body>\n<h2> ' +
        'The time is: </h2>\n<p> %s <p>\n</body>\n</http>\n""" % time_str\n\nprint(html)\n')

    ],
    [
        ".txt",
        ("GET webroot/sample.txt HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        ("This is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.")
    ],
    [
        ".png",
        ("GET webroot/images/sample_1.png HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        png_file_read
    ],
    [
        ".jpg",
        ("GET webroot/images/Sample_Scene_Balls.jpg HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n"),
        jpg_file_read
    ],
]


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

PARAM_404_Request = [
    [
        "404",
        ("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n")
    ]
]


@pytest.mark.parametrize("status, req", REQUESTS)
def test_method_validation(status, req):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    from server import method_validation
    valid = method_validation(req)
    if status == "method":
        valid = not valid
    assert valid


@pytest.mark.parametrize("status, req", REQUESTS)
def test_version_validation(status, req):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    from server import version_validation
    valid = version_validation(req)
    if status == "version":
        valid = not valid
    assert valid


@pytest.mark.parametrize("status, req", REQUESTS)
def test_host_validation(status, req):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    from server import host_validation
    valid = host_validation(req)
    if status == "host":
        valid = not valid
    assert valid


@pytest.mark.parametrize("status, req", REQUESTS)
def test_format_validation(status, req):
    """Tests to see if GET requests are valid and any other type of requests are invalid."""
    from server import format_validation
    valid = format_validation(req)
    if status == "format":
        valid = not valid
    assert valid


@pytest.mark.parametrize("file_type, req, body", GOOD_REQUESTS)
def test_check_ok_response(file_type, req, body):
    """Tests to see if file paths in request return correct files"""
    from server import parse_request
    assert parse_request(req) == ("HTTP/1.1 200 OK\r\n" +
                                "Date: Mon, 23 May 2005 22:38:34 GMT\r\n" +
                                "Server: Apache/1.3.3.7 (Unix) (Red-Hat/Linux)\r\n" +
                                "Last-Modified: Wed, 08 Jan 2003 23:11:55 GMT\r\n" +
                                "Etag: '3f80f-1b6-3e1cb03b'\r\n" +
                                "Accept-Ranges:  none\r\n" +
                                "Content-Length: " + str(len(body)) + "\r\n" +
                                "Connection: close\r\n" +
                                "Content-Type: " + file_type + "\r\n" +
                                "\r\n" + body)


def test_check_404():
    """Tests to see if a request with a file not in the directory
    returns a 404 file not found response."""
    from server import parse_request
    assert parse_request("GET /teddy/bear.html HTTP/1.1\r\n" +
        "Date: Mon, 27 Jul 1884 12:28:53 GMT\r\n" +
        "Server: Teddy Bear\r\n" +
        "Host:  \r\n") == ("HTTP/1.1 404 File Not Found\r\n" +
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

# uncomment below to run server tests

# def test_response_ok():
#     """Tests to see if valid client request will return a 200 OK message."""
#     from client import client
#     assert client("GET hello", 5007) == response


# def test_response_failed():
#     """Tests to see if invalid client request will return a 500 Error message"""
#     from client import client
#     assert client("fuck you.", 5008) == response
