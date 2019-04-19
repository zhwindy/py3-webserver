#!/usr/bin/env python
# encoding=utf-8
import time
import sys
import socket
from io import StringIO
import importlib


class WSGIServer(object):

    FAMILY = (socket.AF_INET, socket.SOCK_STREAM)
    MAX_REQUEST_SIZE = 1
    SOCK_OPT = (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self, address):
        self.listen_socket = socket.socket(*self.FAMILY)
        self.listen_socket.setsockopt(*self.SOCK_OPT)
        self.listen_socket.bind(address)
        self.listen_socket.listen(self.MAX_REQUEST_SIZE)
        host, port = self.listen_socket.getsockname()
        self.server_name = host
        self.port = port

        self.headres_set = []

    def set_application(self, application):
        """
        设置app
        """
        self.application = application

    def start_response(self, status_code, response_header, exc_info=None):
        """
        开始响应
        """
        server_header = [
            ("DATE", "2019-04-19 11:22:33"),
            ("SERVER", "Zhao Pengfei WSGI Server")
        ]

        self.headres_set = [status_code, response_header + server_header]

    def server_forver(self):
        listen_socket = self.listen_socket
        while True:
            self.client_connect, _ = listen_socket.accept()
            self.handle_one_request()

    def parse_request(self, data):
        request = data.splitlines()[0]
        request = request.rstrip("\r\n")
        self.request_method, self.path, self.version = request.split()
    
    def handle_one_request(self):
        """
        处理请求
        """
        request_data = self.client_connect.recv(1024)
        self.request_data = request_data.decode()
        self.parse_request(self.request_data)

        env = self.get_environ()

        response_body = self.application(env, self.start_response)
        self.finsh_response(response_body)

        self.client_connect.close()
    
    def finsh_response(self, response_body):
        status, respone_header = self.headres_set
        response = "HTTP/1.1 {status} \r\\n".format(status=status)
        for k, v in respone_header:
            tmp = k + ":" + v + "\r\\n"
            response += tmp
        response += "\r\\n"
        for txt in response_body:
            response += txt.decode()

        self.client_connect.sendall(response.encode())

    def get_environ(self):
        """
        封装环境变量
        """
        env = {}
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False

        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path
        env['SERVER_NAME'] = self.server_name
        env['SERVER_PORT'] = str(self.port)

        return env


def main_server(address, application):
    server = WSGIServer(address)
    server.set_application(application)
    return server


SERVER_ADDRESS = (HOST, PORT) = "localhost", 9090

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("wsgi need an app to server")
    else:
        args = sys.argv[1]
        module, app = args.split(":")
        module = importlib.import_module(module)
        httpd = main_server(SERVER_ADDRESS, module.app)
        print("WSGI start at port {}".format(PORT))
        httpd.server_forver()
