# coding: utf-8

import tornado.ioloop
import tornado.web
import os
from record_manager import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
    	record_manager = RecordManager(RecordManager.TABLE)
        records = record_manager.show_all()
        # self.write("record is {{records}}")
        self.render("index.html", records=records)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    # "login_url": "/login",
    # "xsrf_cookies": True,
}

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler), 
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8820)
    tornado.ioloop.IOLoop.current().start()