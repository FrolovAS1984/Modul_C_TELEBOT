import telebot

from config import *
from extensions import Convertor, ApiException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = '''
Приветствуем! Наш бот умеет переводить некоторое количество актуальных валют)
Для конвертации отправьте сообщение боту в виде:
<имя валюты, цену которой вы хотите узнать> 
<имя валюты, в которой надо узнать цену первой валюты>  
<количество первой валюты> 
Запрос боту нужно отправлять одной строкой, разделяя позиции пробелом, например:\n
доллар рубль 100
           '''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def start(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in Currency.keys():
        text = '\n'.join((text, i))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise ApiException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except ApiException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, f"Цена {values[2]} {values[0]} в {values[1]} : {answer}")


bot.polling()
