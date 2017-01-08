from threading import Thread
import config

import telebot, time


bot = telebot.TeleBot(config.token)
users=set()

@bot.message_handler(commands=["spam"])
def handle_start_spam(message):
    users.add(message.chat.id)
    bot.send_message(message.chat.id, "Спамим кароч")

@bot.message_handler(commands=['stop'])
def handle_stop_spam(message):
    users.remove(message.chat.id)
    bot.send_message(message.chat.id, "Ок, без базара")
@bot.message_handler(content_types=['text'])
def doIt(message):
    result = eval(message.getText())
    bot.send_message(message.chat.id, str(result))

def spam():
    global users
    while True:
        for user in users:
            print(user)
            bot.send_message(user, "Спамим")
        time.sleep(0.5)
def polling():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    thread = Thread(target=spam)
    thread.start()
    thread1 = Thread(target=polling)
    thread1.start()

