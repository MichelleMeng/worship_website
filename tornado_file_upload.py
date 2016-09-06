# coding: utf-8

import tornado.ioloop
import tornado.web
import os
import time
from record_manager import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_files.html")

    def post(self):
    	rcdfile = self.request.files['record']
    	time_now = time.strftime("%Y%m%d%H%M%S_", time.localtime())
        for rcd in rcdfile:
            with open('./static/record/' + time_now + rcd['filename'], 'wb') as f:
                f.write(rcd['body'])
                rcd_link = "/static/record/" + time_now + rcd['filename']
            
        txtfile = self.request.files['text']
        for txt in txtfile:
            with open('./static/text/' + time_now + txt['filename'], 'wb') as f:
                f.write(txt['body'])
                txt_link = "/static/text/" + time_now + txt['filename']
            
        leaffile = self.request.files['leaflet']
        for leaf in leaffile:
            with open('./static/leaflet/' + time_now + leaf['filename'] , 'wb') as f:
                f.write(leaf['body'])
                leaf_link = '/static/leaflet/' + time_now + leaf['filename']
        
        self.write('Upload finished')
        record_manager = RecordManager(RecordManager.TABLE)
        record_manager.add('2016-9-2', 'title_test', rcd_link, txt_link, leaf_link)



application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
	try: 
	    app = application
	    app.listen(8895)
	    tornado.ioloop.IOLoop.current().start()
	except Exception, e:
		traceback.print_exc()