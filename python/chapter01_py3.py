#! /usr/bin/env python
# encoding=utf-8
from http.server import SimpleHTTPRequestHandler
import socketserver

HOST, PORT = "localhost", 9000


def http_server():
    with socketserver.TCPServer((HOST, PORT), SimpleHTTPRequestHandler) as httpd:
        print("Http Server at port {}".format(PORT))
        httpd.serve_forever()


if __name__ == '__main__':
    http_server()
