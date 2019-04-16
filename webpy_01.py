#!/usr/bin/env python
# encoding=utf-8
import web

urls = (
    '/(.*)', 'hello'
)

app = web.application(urls, globals())


class hello(object):

    def GET(self, name):
        return 'Hello' + name + '!'


if __name__ == '__main__':
    app.run()
