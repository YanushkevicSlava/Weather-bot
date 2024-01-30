import telebot
import json
import requests
from telebot import types
from tokens import token, api

bot = telebot.TeleBot(token)
API = api


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('London')
    btn2 = types.KeyboardButton('Moscow')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Tokio')
    btn4 = types.KeyboardButton('New York')
    markup.row(btn3, btn4)
    btn5 = types.KeyboardButton('Minsk')
    btn6 = types.KeyboardButton('Berlin')
    markup.row(btn5, btn6)
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} {message.from_user.last_name}!\n'
                                      f'Введите название города: ', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if data.status_code == 200:
        weather_data = json.loads(data.text)
        temperature = weather_data['main']['temp']
        feels = weather_data['main']['feels_like']
        wind = weather_data['wind']['speed']
        bot.send_message(message.chat.id, f'Погода в {city.title()}:\n'
                                          f'Температура: {temperature}, ощущается {feels}\n'
                                          f'Скорость ветра: {wind} м/с')
    else:
        bot.send_message(message.chat.id, 'Такого города не существует!!!\n'
                                          'Введите название города:')


bot.infinity_polling()
