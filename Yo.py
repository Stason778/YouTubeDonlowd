import os

import telebot
import  Token
from pytube import YouTube
bot = telebot.TeleBot(Token.Token)

@bot.message_handler(commands=['start'])
def welcome(message):
	chat_id = message.chat.id
	mess = f'Привіт {message.from_user.first_name} '
	bot.send_message(message.chat.id,mess)



@bot.message_handler(func=lambda m: True)
def text_message(message):
	chat_id = message.chat.id
	url = print(message.text)
	if message.text.startswith('https://youtu.be/') :
		bot.send_message(chat_id,'Починаю завантаження', parse_mode='html' )
		download_youtube_video(message.text, message, bot)




def download_youtube_video(url, message, bot):
	yt = YouTube(url)
	stream = yt.streams.filter(progressive=True, file_extension='mp4')
	stream.get_highest_resolution().download(f'{message.chat.id}{yt.title}')
	with open(f"{message.chat.id}{yt.title}/{yt.title}.mp4") as video:
		bot.send_document(message.chat.id,video,caption="*Ось ваше відео*")
		os.remove(f"{message.chat.id}{yt.title}")
filel = r'C:\Users\IdeaPad\q\all_questions.txt'
with open(filel) as f:
	reader = f.read()
	print(reader)

bot.polling(none_stop=True)



