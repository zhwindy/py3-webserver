#!/usr/bin/env python
# encoding=utf-8
import socket

SERVER_ADDRESS = (HOST, PORT) = "", 8888


def request():
    request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request_socket.connect(SERVER_ADDRESS)
    request_socket.send(b"GET / HTTP/1.1")
    recv = request_socket.recv(1024)
    print(recv.decode("utf-8"))


if __name__ == "__main__":
    request()
