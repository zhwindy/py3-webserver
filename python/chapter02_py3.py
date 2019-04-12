#!/usr/bin/env python
# encoding=utf-8
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST, PORT = "", 9000


class test_httpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        message = "Hello World!"
        self.wfile.write(bytes(message, 'utf-8'))
        return


def run_server():
    http_server = HTTPServer((HOST, PORT), test_httpRequestHandler)
    print("HTTP Server start at port {}".format(PORT))
    http_server.serve_forever()


if __name__ == "__main__":
    run_server()
