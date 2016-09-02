# coding: utf-8

import tornado.ioloop
import tornado.web
import os
import time

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload_files.html")

    def post(self):
    	rcdfile = self.request.files['record']
        for rcd in rcdfile:
            with open('./static/record/' + rcd['filename'], 'wb') as f:
                f.write(rcd['body'])
            
        txtfile = self.request.files['text']
        for txt in txtfile:
            with open('./static/text/' + txt['filename'], 'wb') as f:
                f.write(txt['body'])
            
        leaffile = self.request.files['leaflet']
        for leaf in leaffile:
            with open('./static/leaflet/' + time.strftime("%Y%m%d%H%M%S_", time.localtime()) + leaf['filename'] , 'wb') as f:
                f.write(leaf['body'])
        
        self.write('Upload finished')


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    app = application
    app.listen(8891)
    tornado.ioloop.IOLoop.current().start()