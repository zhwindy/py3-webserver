#!/usr/bin/env python
# encoding=utf-8
import socket
import os
import time

SERVER_ADDRESS = (HOST, PORT) = "", 8888
MAX_QUEUE_SIZE = 5


def handle_one_request(client):
    request_data = client.recv(1024)
    print("Child Pid: {}, Parent Pid: {}".format(os.getpid(), os.getppid()))
    print(request_data.decode())

    response = b"""
HTTP/1.1 200 OK

Welcome to visit webservice_03
    """
    client.sendall(response)
    time.sleep(60)


def run_server():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(MAX_QUEUE_SIZE)
    print("Http Server is start on port {}".format(PORT))
    print("Parent Pid: {}".format(os.getpid()))

    while True:
        conn, _ = listen_socket.accept()
        pid = os.fork()
        if pid == 0:
            listen_socket.close()
            handle_one_request(conn)
            conn.close()
            os._exit(0)
        else:
            conn.close()


if __name__ == "__main__":
    run_server()
