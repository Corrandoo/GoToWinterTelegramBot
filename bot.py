import json
from threading import Thread
import config
import telebot, time, datetime
schedule = []

def clearSchedule():
    global schedule
    schedule = []


bot = telebot.TeleBot(config.token)
users=set()
fle = open("timetable.txt", "r", encoding="utf8")
text = fle.read().split("\n")

for t in text:
    te = t.split("=")
    schedule.append({'time': te[0], 'name': te[1]})


def checkEventNow(event):
    now_time = datetime.datetime.now()
    nhour = now_time.hour
    nminute = now_time.minute
    ehours = event['time'].split(":")[0]
    eminutes = event['time'].split(":")[1]
    if str(nhour) == str(ehours) and str(nminute) == str(eminutes):
        return event
    return False
def eventWriter():
    global schedule
    while True:
        for event in schedule:
            print(event)
            if checkEventNow(event) == False:
                pass
            else:
                for user in users:
                    bot.send_message(user, "Внимание! Событие " + event['name'] + " начинается сейчас!!!")
        time.sleep(59)


@bot.message_handler(commands=["subscribe"])
def handle_add_goto_timetable(message):
    users.add(message.chat.id)
    bot.send_message(message.chat.id, "Вы добавлены в рассылку расписания GoTo!")
@bot.message_handler(commands=["unsubscribe"])
def handle_unsubscribe_goto_timetable(message):
    users.remove(message.chat.id)
    bot.send_message(message.chat.id, "Вы удалены из рассылки расписания GoTo.")


@bot.message_handler(content_types=['text'])
def doIt(message):
    result = eval(message.getText())
    bot.send_message(message.chat.id, str(result))



def polling():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    thread1 = Thread(target=polling)
    thread1.start()
    thread2 = Thread(target=eventWriter)
    thread2.start()

