import json
from threading import Thread
import config
import telebot, time, datetime
schedule = []

def fillUsersFromFile():
    global users
    usfile = open("users.txt", "r", encoding="utf8")
    strUsers = usfile.read().split("//")
    users.clear()
    for suser in strUsers:
        users.append(int(suser))

bot = telebot.TeleBot(config.token)
users = []
fillUsersFromFile()
fle = open("timetable.txt", "r", encoding="utf8")
text = fle.read().split("\n")
botHumor = 0

for t in text:
    te = t.split("=")
    schedule.append({'time': te[0], 'name': te[1]})


def addUserToList():
    global users
    usfile = open("users.txt", "w", encoding="utf8")
    for user in users:
        if user != users[-1] or len(users) == 1:
            usfile.write(str(user) + "//")
        else:
            usfile.write(str(user))
def removeUserFromList():
    global users
    usfile = open("users.txt", "w", encoding="utf8")
    for user in users:
        if user != users[-1] or len(users) == 1:
            usfile.write(str(user) + "//")
        else:
            usfile.write(str(user))


def checkEventNow(event):
    try:
        now_time = datetime.datetime.now()
        nhour = now_time.hour
        nminute = now_time.minute
        ehours = event['time'].split(":")[0]
        eminutes = event['time'].split(":")[1]
        if str(nhour) == str(ehours) and str(nminute) == str(eminutes):
            return event
        return False
    except:
        pass
def eventWriter():
    global schedule
    while True:
        for event in schedule:
            print(event)
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
    for user in users:
        if user == message.chat.id:
            bot.send_message(user, "Вы уже добавлялись в рассылку расписания GoTo!")
            return
    users.append(message.chat.id)
    bot.send_message(message.chat.id, "Вы добавлены в рассылку расписания GoTo!")
    addUserToList()

@bot.message_handler(commands=["unsubscribe"])
def handle_unsubscribe_goto_timetable(message):
    for user in users:
        if message.chat.id == user:
            users.remove(message.chat.id)
            bot.send_message(message.chat.id, "Вы удалены из рассылки расписания GoTo.")
            removeUserFromList()
    bot.send_message(message.chat.id, "Вы уже удалялись из рассылки расписания GoTo.")



'''@bot.message_handler(commands=['changehumor7712'])
def handle_changeHumor_message(message):
    sent = bot.send_message(message.chat.id, "Введите уровень юмора от 0 до 2")
    bot.register_next_step_handler(sent, get_humor_level)

def get_humor_level(message):
    global botHumor
    if int(message.getText()) > 2 or int(message.getText()) < 0:
        botHumor = 0
        bot.send_message(message.chat.id, "Вы указали неправильный уровень юмора. Текущий равен 0.")
    else:
        botHumor = int(message.getText())'''
def polling():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    thread1 = Thread(target=polling)
    thread1.start()
    thread2 = Thread(target=eventWriter)
    thread2.start()