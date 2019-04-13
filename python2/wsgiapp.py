#!/usr/bin/env python
# encoding=utf-8


def app(envison, start_response):
    status = 200

    request_header = [("Content-Type", "text/plain")]

    start_response(status, request_header)

    return "Hello World from simple WSGI application"
