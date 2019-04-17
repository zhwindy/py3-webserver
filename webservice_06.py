#!/usr/bin/env python
# encoding=utf-8
import time
import sys
import socket

SERVER_ADDRESS = (HOST, PORT) = "localhost", 9090
MAX_REQUEST_SIZE = 256


class WSGIServer(object):

    def __init__(self, app):
        self.set_application(app)
        self.listen_socket = None
        self.request_headres = []

    def set_application(self, app):
        self.application = app
    
    def start_response(self, env):
        """
        组织响应
        """
        pass

    def server_forver(self):
        self.listen_socket = listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(SERVER_ADDRESS)
        listen_socket.listen(MAX_REQUEST_SIZE)

        while True:
            client_connect, _ = listen_socket.accept()
            request_data = client_connect.recv(1024)
            self.handle_one_request(request_data)
            client_connect.close()
    
    def handle_one_request(self, request):
        env = self.get_environ(request)

        response_body = self.application(env, self.start_response)
        self.finsh_response(response_body)
    
    def finsh_response(self, text):

        self.listen_socket.sendall(text)

    def get_environ(self, request):
        env = {}
        env['wsgi.version'] = 'HTTP /1.1'
        env['wsgi.method'] = 'GET'
        env['wsgi.path'] = '/'

        return env


def main_server(app):
    server = WSGIServer(app)
    return server


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("wsgi need an app to server")
    args = sys.argv[1]
    moudle, app = args.split(":")
    httpd = main_server(app)
    httpd.server_forver()
