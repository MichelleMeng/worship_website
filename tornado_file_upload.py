# coding: utf-8

import tornado.ioloop
import tornado.web
import os
import time
from record_manager import *

record_manager1 = RecordManager(RecordManager.TABLE)
class ListAllHandler(tornado.web.RequestHandler):
    def get(self):
        records = record_manager1.show_all()
        self.render("upload_list.html", records=records)


class CreateNewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_files.html")

    def post(self):
    	worshipdate = self.get_argument('date')
    	themeofweek = self.get_argument('title')

    	rcdfile = self.request.files['record']
    	# time_now = time.strftime("%Y%m%d%H%M%S_", time.localtime())
        for rcd in rcdfile:
            rcdname = rcd['filename'].replace(' ','_')
            with open('./static/record/' + rcdname, 'wb') as f:
                f.write(rcd['body'])
                rcd_link = "record/" + rcdname
            
        txtfile = self.request.files['text']
        for txt in txtfile:
            txtname = txt['filename'].replace(' ','_')
            with open('./static/text/' + txtname, 'wb') as f:
                f.write(txt['body'])
                txt_link = "text/" + txtname
            
        leaffile = self.request.files['leaflet']
        for leaf in leaffile:
            leafname = leaf['filename'].replace(' ','_')
            with open('./static/leaflet/' + leafname, 'wb') as f:
                f.write(leaf['body'])
                leaf_link = 'leaflet/' + leafname
        
        self.redirect("/admin/upload_finish")
        record_manager = RecordManager(RecordManager.TABLE)
        record_manager.add(worshipdate, themeofweek, rcd_link, txt_link, leaf_link)


class UploadFinishHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_finished.html")


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    # "login_url": "/login",
    # "xsrf_cookies": True,
}


application = tornado.web.Application([
    (r"/admin/view_all", ListAllHandler),
    (r"/admin/create_new", CreateNewHandler),
    (r"/admin/upload_finish", UploadFinishHandler)
], **settings)



if __name__ == "__main__":
	try: 
	    app = application
	    app.listen(8893)
	    tornado.ioloop.IOLoop.current().start()
	except Exception, e:
		traceback.print_exc()