"""Tests to make sure client and server can communicate via sockets."""


import pytest
import client
import server


# def test1():
#     """Test if string that is shorter than buffer length gets sent."""
#     assert client.client("hello") == "hello"


def test2():
    """Test if string that is longer than buffer length gets sent."""
    assert client.client("I don't know why you say 'goodbye' I say 'hello'") == "I don't know why you say 'goodbye' I say 'hello'"


def test3():
    """Test if string that is longer than buffer length gets sent."""
    assert client.client("hlo gdby") == "hlo gdby"


def test4():
    """Test if string that is longer than buffer length gets sent."""
    assert client.client("¡¢£¤¥") == "¡¢£¤¥"
