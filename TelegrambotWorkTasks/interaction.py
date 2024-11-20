from keyboard import Keyboards
from utils import create_bot

bot = create_bot()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = Keyboards().registration()
    bot.send_message(message.chat.id, 'Кто ты воин?', reply_markup=keyboard)
    # print('Поздоровались.')


@bot.message_handler(commands=['start', 'help'])
def mine(message):
    keyboard = Keyboards().registration_keyboard()
    bot.send_message(message.chat.id, 'Кто ты воин?', reply_markup=keyboard)
    # print('Поздоровались.')