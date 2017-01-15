import tornado.ioloop
import tornado.web
import bot

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('first.html', message="")
    def post(self):
        clear = self.get_argument('doTimetableClear', 'false')
        newTimetable = self.get_argument('timetable', 'none')
        doWithTt = self.get_argument('whatDoWithNewTimetable', 'none')
        if clear == 'true':
            bot.clearTimetableList()
        if newTimetable == '\n':
            pass
        else:
            if doWithTt == 'rewrite':
                ttfile = open('timetable.txt', 'w', encoding='utf8')
                ttfile.write(newTimetable)
            elif doWithTt == 'append':
                ttfile = open('timetable.txt', 'a', encoding='utf8')
                ttfile.write("\n")
                ttfile.write(newTimetable)
        self.render('first.html', message="Выполнено")


settings = [
    ('/', MainHandler)
]

app = tornado.web.Application(settings)
app.listen(8888)
tornado.ioloop.IOLoop.current().start()