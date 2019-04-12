#!/usr/bin/env python
# encoding=utf-8
from flask import Flask, Response

flask_app = Flask("flaskapp")


@flask_app.route("/")
def index():
    message = "Hello world \n"
    return Response(message, mimetype='text/plain')


@flask_app.route("/hello")
def hello():
    message = "Hello My flask app \n"
    return Response(message, mimetype='text/plain')


app = flask_app.wsgi_app


if __name__ == "__main__":
    flask_app.run()
