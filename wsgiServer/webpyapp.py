#!/usr/bin/env python
# encoding=utf-8
import web

urls = (
    '/(.*)', 'hello'
)

application = web.application(urls, globals())


class hello(object):

    def GET(self, name):
        return 'Hello' + name + '!'


app = application.wsgifunc()

if __name__ == '__main__':
    application.run()
