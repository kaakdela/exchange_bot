import telebot
import requests
import json
from config import TOKEN, keys
from extensions import Convertor, ConverterExceptions


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n "евро" ' \
           '<в какую валюту перевести> <количество переводимой валюты> \n увидеть список доступных валют - /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
      text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))
    try:
        result = Convertor.get_price(values)
    except ConverterExceptions as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
    else:
        text = f'Цена {values[0]} {values[1]} в {values[2]} -- {result} {keys[values[1]]}'
        bot.reply_to(message, text)
bot.polling(none_stop=True, interval=0)

