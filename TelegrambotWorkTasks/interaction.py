from keyboard import Keyboards
from utils import create_bot

bot = create_bot()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = Keyboards().registration_keyboard()
    bot.send_message(message.chat.id, 'Кто ты воин?', reply_markup=keyboard)


# Начальное сообщение менеджерам.
@bot.message_handler(commands=['start', 'help'])
def manager(message):
    keyboard = Keyboards().manager_keyboard()
    bot.send_message(message.chat.id, 'Добро пожаловать.', reply_markup=keyboard)


# Начальное сообщение водителям.
@bot.message_handler(commands=['start', 'help'])
def driver(message):
    keyboard = Keyboards().driver_keyboard()
    bot.send_message(message.chat.id, 'Добро пожаловать.', reply_markup=keyboard)


