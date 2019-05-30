#!/usr/bin/env python
# encoding=utf-8
from flask import Flask, Response
import time

flask_app = Flask("flaskapp")


@flask_app.route("/")
def index():
    message = "Hello world \r\n"
    return Response(message, mimetype='text/plain')


@flask_app.route("/hello")
def hello():
    message = "Hello My flask app \r\n"
    time.sleep(1)
    return Response(message, mimetype='text/plain')


app = flask_app.wsgi_app


if __name__ == "__main__":
    flask_app.run(debug=True)
