from utils import create_bot, get_db_connection
from interaction import send_welcome
from database import check_and_create_tables

# Подключение к боту.
bot = create_bot()

try:
    # Получаем соединение с базой данных
    cnx, cursor = get_db_connection()

    # Проверяем и создаем таблицы если необходимо
    check_and_create_tables(cursor)
    cnx.commit()  # Применяем изменения

except ConnectionError as e:
    print(f"Ошибка при подключении к базе данных: {e}")
    exit(1)

users_data = {}


@bot.message_handler(func=lambda message: True)
def entrance(message):
    print(f'Сообщение: {message}')
    print(f'{message.from_user.first_name} вошел в систему.\n')

    user_id = str(message.from_user.id)
    print(f'{user_id} вошел в чат.')

    # Отправляем сообщение пользователю. 476822305 476822305
    send_welcome(message)


user = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = str(call.message.chat.id)
    print(f'chat_id: {chat_id}')
    if call.data == 'knight':
        print("knight")

        pass
        bot.send_message(call.message.chat.id, 'Введите имя и фамилию.')
        # print('Введите имя')
        # bot.register_next_step_handler(call.message, handle_first_name_input, users_data, chat_id)
    elif call.data == 'mouse':
        print("mouse")
        bot.send_message(call.message.chat.id, 'Возвращайтесь если передумаете.')
        pass


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    finally:
        # Закрываем соединение с базой данных после завершения работы бота
        cursor.close()
        cnx.close()
