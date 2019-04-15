#!/usr/bin/env python
# encoding=utf-8
import socket
import errno
import os
import argparse


SERVER_ADDRESS = (HOST, PORT) = "", 8888


def main(max_clients, max_conns):
    socks = []
    print(20*"#", max_clients, max_conns)
    for _ in range(max_clients):
        pid = os.fork()
        if pid == 0:
            for conn_num in range(max_conns):
                request_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                request_socket.connect(SERVER_ADDRESS)
                request_socket.send(b"GET / HTTP/1.1")
                socks.append(request_socket)
                print(20 * "*", conn_num)
                os._exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-clients", type=int, default=1, help="最大并发数")
    parser.add_argument("--max-conns", type=int, default=1024, help="最大连接数")
    args = parser.parse_args()
    main(args.max_clients, args.max_conns)
