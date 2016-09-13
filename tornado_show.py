# coding: utf-8

import tornado.ioloop
import tornado.web
import os
from record_manager import *

record_manager = RecordManager(RecordManager.TABLE)
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        records = record_manager.show_all()
        self.render("index.html", records=records)

class EntryHandler(tornado.web.RequestHandler):
	def get(self, entry_id):
		entry = record_manager.get_by_id(entry_id)
		self.render("worship.html", record = entry[0])

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    # "login_url": "/login",
    # "xsrf_cookies": True,
}

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler), 
        (r"/entry/([0-9a-zA-Z-]+)", EntryHandler) # 只要url是这样的格式"/entry/([0-9a-zA-Z-]+)"，都调用EntryHandler
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8802)
    tornado.ioloop.IOLoop.current().start()
