from utils import create_bot, get_db_connection
from interaction import send_welcome

# Подключение к боту.
bot = create_bot()

try:
    # Получаем соединение с базой данных
    cnx, cursor = get_db_connection()
except ConnectionError as e:
    print(f"Ошибка при подключении к базе данных: {e}")
    exit(1)

users_data = {}


@bot.message_handler(func=lambda message: True)
def entrance(message):
    print(f'Сообщение: {message}')
    print(f'{message.from_user.first_name} вошел в систему.')

    chat_id = str(message.chat.id)
    users_data[chat_id] = {'first_last_name': '', 'phone': '', 'spec': '', 'about': '', 'photo': ''}

    send_welcome(message)


cursor.close()
cnx.close()

if __name__ == "__main__":
    bot.polling(none_stop=True)