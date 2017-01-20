# -*- coding: utf-8 -*-

from threading import Thread
import config, database_connector
import telebot, time, datetime
schedule = []
users = []
usernames = {}
bot = telebot.TeleBot(config.token)

def polling():
    bot.polling(none_stop=True)

def clearTimetableList():
    global schedule
    schedule = []
    open("timetable.txt", "w", encoding="utf8")


def checkEventNow(event):
    try:
        now_time = datetime.datetime.now()
        nhour = now_time.hour
        nminute = now_time.minute
        ehours = event['time'].split(":")[0]
        eminutes = event['time'].split(":")[1]
        if str(nhour) == str(ehours) and str(nminute) == str(eminutes):
            return event
        if int(eminutes) - int(nminute) == 5 and int(ehours) - int(nhour) == 0 or (int(eminutes) == 0 and int(ehours) - int(nhour) == 1 and int(nminute) - int(eminutes) == 55):
            for user in users:
                bot.send_message(user, "Внимание! Событие " + event['name'] + " начинается через 5 минут!")
        return False
    except:
        pass
def eventWriter():
    global schedule
    while True:
        for event in schedule:
            if checkEventNow(event) == False:
                pass
            else:
                for user in users:
                    if botHumor == 0:
                        bot.send_message(user, "Внимание! Событие " + event['name'] + " начинается сейчас!!!")
                    elif botHumor == 1:
                        bot.send_message(user, "Ребята! Все бежим на " + event['name'] + "! Уже начинаем!")
                    elif botHumor == 2:
                        bot.send_message(user, "Чуваки! Гоним быстрее на " + event['name'] + ", а то начнем без вас!")
        time.sleep(59)


@bot.message_handler(commands=["subscribe"])
def handle_add_goto_timetable(message):
    first_name = bot.get_chat(message.chat.id).first_name
    last_name = bot.get_chat(message.chat.id).last_name
    username = bot.get_chat(message.chat.id).username
    database_connector.add_new_user_to_database(message.chat.id, first_name, last_name, username)


    for user in users:
        if user == message.chat.id:
            bot.send_message(user, "Вы уже добавлялись в рассылку расписания GoTo!")
            return
    users.append(message.chat.id)
    bot.send_message(message.chat.id, "Вы добавлены в рассылку расписания GoTo!")

@bot.message_handler(commands=["unsubscribe"])
def handle_unsubscribe_goto_timetable(message):
    database_connector.remove_user_from_database(message.chat.id)
    for user in users:
        if message.chat.id == user:
            users.remove(message.chat.id)
            bot.send_message(message.chat.id, "Вы удалены из рассылки расписания GoTo.")
            return
    bot.send_message(message.chat.id, "Вы уже удалялись из рассылки расписания GoTo.")
@bot.message_handler(commands=["start", "help"])
def welcome_message(message):
    bot.send_message(message.chat.id, "Привет! Я - бот расписания школы GoTo!")
    bot.send_message(message.chat.id, "Я отсылаю информацию о каждом событии во время его начала.")
    bot.send_message(message.chat.id, "Напишите /subscribe, чтобы подписаться на рассылку. /unsubscribe, чтобы отписаться")
    bot.send_message(message.chat.id, "Напишите /howedit , чтобы получить справку о том, как меня заполнять.")
    bot.send_message(message.chat.id, "Напишите /timetable , чтобы получить все расписание на сегодня.")
@bot.message_handler(commands=["howedit"])
def printGuide(message):
    bot.send_message(message.chat.id, "Для редактирования рассылаемого расписания используйте файл timetable.txt")
    bot.send_message(message.chat.id, "Каждое событие пишется с новой строки.")
    bot.send_message(message.chat.id, "Между часами и минутами ставится двоеточие.")
    bot.send_message(message.chat.id, "Если количество часов или минут меньше 10, то кол-во часов и минут пишется без нуля")
    bot.send_message(message.chat.id, "Между временем события и его названием ставится =")
    bot.send_message(message.chat.id, "Пример: 8:5=Подъем!")
    bot.send_message(message.chat.id, "11:25=Перерыв")

@bot.message_handler(commands=["timetable"])
def printTimetable(message):
    user = message.chat.id
    for event in schedule:
        bot.send_message(user, event['time'] + " " + event['name'])
        time.sleep(0.5)


fle = open("timetable.txt", "r", encoding="utf8")
text = fle.read().split("\n")
botHumor = 0
try:
    for t in text:
        te = t.split("=")
        tt = te[0].split("")
        try:
            if tt[0] == '0' and tt[2] == ':':
                te[0] = tt[1] + tt[2] + tt[3] + tt[4]
        except:
            te[0] = tt[1]+tt[2]+tt[3]
        schedule.append({'time': te[0], 'name': te[1]})
except:
    schedule = []

if __name__ == '__main__':
    thread1 = Thread(target=polling)
    thread1.start()
    thread2 = Thread(target=eventWriter)
    thread2.start()