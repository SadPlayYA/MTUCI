import telebot
import commands as comm
import time



# свой токен вставляем в data/bot/token.txt
# инициализируем бота
bot = telebot.TeleBot(comm.get_info_for_bot('token'))


#<commands>
# в случае нажатия команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, comm.get_info_for_bot())
    time.sleep(2)
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row("Узнать свежую информацию", "/help", "/find_film", "/music",  "/photo")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?\nЕсли да, жми кнопку!', reply_markup=keyboard)


# в случае нажатия команды /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, comm.get_info_for_bot('help'))


# в случае нажатия команды /find_film
@bot.message_handler(commands=['find_film'])
def find_film(message):
    data = comm.get_info_of_film()
    bot.send_message(message.chat.id, data[0])
    bot.send_photo(message.chat.id, open(f'data/commands/films/{data[1]}/photo.jpg', 'rb'))


# в случае нажатия команды /music
@bot.message_handler(commands=['music'])
def music(message):
    bot.send_message(message.chat.id, 'Держи: \nhttps://vk.com/audio?z=audio_playlist176916096_83955555')


# в случае нажатия команды /photo
@bot.message_handler(commands=['photo'])
def photo(message):
    bot.send_message(message.chat.id, 'Держи фотку:')
    bot.send_photo(message.chat.id, open(f'data/commands/photo/{comm.get_name()}.jpg', 'rb'))


# для вывода каждого сообщения в консоль
@bot.message_handler(content_types=['text'])
def print_message_of_console(message):
    print(f'{message.chat.username} ({message.chat.first_name})| написал - "{message.text}"')
    if message.text.lower() == 'узнать свежую информацию':
        bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')
    else:
        bot.send_message(message.chat.id, 'ЙА ТЕБЯ НЕ ПОНИМАТЬ!')
        bot.send_message(message.chat.id, comm.emoji())



# чтобы бот работал
bot.polling(none_stop=True, interval=0)
