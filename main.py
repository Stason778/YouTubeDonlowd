import os
import time
import telebot
import Token
from pytube import YouTube
from telebot import types
bot = telebot.TeleBot(Token.Token)
URL = 'http://127.0.0.1:8081/bot%3C6181298977:AAGMLWuSwZDq-LOEm1e2xinTl2pT_Ek_x1U%3E/sendVideo'
user_list = {}
content_map = {'audio':'mp3','video':'mp4'}

class User:
    def __init__(self, chat_id, content_type):
        self.chat_id = chat_id
        self.content_type = content_type

    def yt(self, url, message, bot,file_extension):
        if self.content_type == 'audio':
            download_youtube_content_type(url, message, bot, file_extension)
        else:
            download_youtube_content_type(url, message, bot, file_extension)

    @staticmethod
    def get_or_create(chat_id):
        if user_list.get(chat_id):
            return user_list.get(chat_id)
        user = User(chat_id, 'video')
        user_list[chat_id] = user
        return user
'''git rm text.txt # видалити неіндексований файл (файл буде видалений з папки)

git rm -f text.txt # видалити індексований файл (файл буде видалений з папки)

git rm -r log/ # видалити весь вміст папки log/ (папка буде видалена)'''

@bot.message_handler(commands=['start'])
def welcome(message):
    mess = f'Привіт {message.from_user.first_name} , Відправляй посилання: '
    bot.send_message(message.chat.id, mess)

'''@bot.message_handler(commands=['button'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('відео',callback_data='video')
    item1 = types.InlineKeyboardButton('аудіо',callback_data='audio')
    markup.add(item, item1)
    bot.send_message(message.chat_id,'Привіт',reply_markup=markup)
@bot.message_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'audio':
            bot.send_message(call.message.chat_id,audio)'''
@bot.message_handler(commands=['audio'])
def audio(message):
    user = User.get_or_create(message.chat.id)
    user.content_type = 'audio'
    bot.send_message('audio')


@bot.message_handler(commands=['video'])
def video(message):
    user = User.get_or_create(message.chat.id)
    user.content_type = 'video'


@bot.message_handler(func=lambda m: True)
def text_message(message):
    chat_id = message.chat.id
    url = message.text
    if message.text.startswith('https://youtu.be/'):
        user = User.get_or_create(chat_id)
        bot.send_message(chat_id, 'Починаю завантаження, це може зайняти деклька хвилин :)')
        user.yt(url, message, bot,content_map.get(user.content_type))


def download_youtube_content_type(url, message, bot, file_extension):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    stream.get_lowest_resolution().download(f'media/{message.chat.id}{yt.title}')
    with open(f"media/{message.chat.id}{yt.title}/{yt.title}.mp4", 'rb') as audio:
        if file_extension == 'mp3':
            bot.send_audio(message.chat.id, audio, caption="Ось ваше музика")
        else:
            bot.send_video(message.chat.id, audio, caption="Ось ваше відео")
    os.remove(f"{message.chat.id}{yt.title}")




@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('video/'):
        if file.split('.')[-1] == 'ogg':
            f = open('video/' + file, 'rb')
            res = bot.send_video(message.chat.id, f)
            print(file, res)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(3)
