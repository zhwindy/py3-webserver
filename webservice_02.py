#!/usr/bin/env python
# encoding=utf-8
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = "", 8888


def handle_one_request(client):
    """
    处理单笔请求
    """
    request = client.recv(1024)
    print(request.decode('utf-8'))
    response = b"""\
HTTP/1.1 200 OK

Hello World from webservice_02
        """
    client.sendall(response)
    time.sleep(30)


def run_server():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen()
    print("Http Server is start on port {}".format(PORT))

    while True:
        client_connection, client_address = listen_socket.accept()
        print(50 * "*", client_address)
        handle_one_request(client_connection)
        client_connection.close()


if __name__ == "__main__":
    run_server()
