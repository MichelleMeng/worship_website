# coding: utf-8

import tornado.ioloop
import tornado.web
import os
from tornado_show import *
from tornado_file_upload import *


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    # "login_url": "/login",
    # "xsrf_cookies": True,
}

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler), 
        (r"/entry/([0-9a-zA-Z-]+)", EntryHandler), # 只要url是这样的格式"/entry/([0-9a-zA-Z-]+)"，都调用EntryHandler
        (r"/admin/view_all", ListAllHandler),
    	(r"/admin/delete/([0-9a-zA-Z-]+)", DeleteHandler),
   		(r"/admin/create_new", CreateNewHandler),
    	(r"/admin/update/([0-9a-zA-Z-]+)", UpdateHandler),
    	(r"/admin/finish", UploadFinishHandler)
    ], **settings)


if __name__ == "__main__":
	try: 
	    app = make_app()
	    app.listen(8802)
	    tornado.ioloop.IOLoop.current().start()
	except Exception, e:
		print e
		# traceback.print_exc()