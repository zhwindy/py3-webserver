#!/usr/bin/env python
# encoding=utf-8
import socket
from io import StringIO
import sys


class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        self.listen_socket = socket.socket(self.address_family, self.socket_type)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(server_address)
        self.listen_socket.listen(self.request_queue_size)
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        self.headers_set = []

    def set_app(self, application):
        """
        设置app
        """
        self.application = application

    def server_forver(self):
        """
        启动服务
        """
        listen_socket = self.listen_socket
        while True:
            self.client_connection, _ = listen_socket.accept()
            self.handle_one_request()
    
    def handle_one_request(self):
        """
        处理一笔请求
        """
        recv = self.client_connection.recv(1024)
        self.request_data = request_data = recv.decode('utf-8')
        print(''.join('<{line}\n'.format(line=line) for line in request_data.splitlines()))
        
        self.parse_request(request_data)

        env = self.get_environ()

        result = self.application(env, self.start_respone)

        self.finish_respone(result)
    
    def parse_request(self, data):
        """
        解析请求
        """
        text_line = data.splitlines()[0]
        text_line = text_line.rstrip('\r\n')
        self.request_method, self.path, self.version = text_line.split()

    def get_environ(self):
        """
        设置环境变量
        """
        env = {}
        # 设置wsgi的必须变量
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # 设置CGI的必须变量
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path
        env['SERVER_NAME'] = self.server_name
        env['SERVER_PORT'] = str(self.server_port)

        return env
    
    def start_respone(self, status, response_headres, exc_info=None):
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headres + server_headers]
    
    def finish_respone(self, result):
        try:
            status, response_headers = self.headers_set
            response = "HTTP/1.1 {status}\r\\n".format(status=status)
            for header in response_headers:
                response += "{0} : {1}\r\\n".format(*header)
            response += "\r\\n"
            for data in result:
                response += data.decode('utf-8')
            print(''.join("> {line} \n".format(line=line) for line in response.splitlines()))
            self.client_connection.sendall(response.encode('utf-8'))
        finally:
            self.client_connection.close()


SERVER_ADDRESS = (HOST, PORT) = "", 8899


def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    moudle, application = app_path.split(":")
    moudle = __import__(moudle)
    application = getattr(moudle, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    httpd.server_forver()
