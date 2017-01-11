import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('first.html')
    def post(self):
        pass

settings = [
    ('/', MainHandler)
]

app = tornado.web.Application(settings)
app.listen(80)
tornado.ioloop.IOLoop.current().start()