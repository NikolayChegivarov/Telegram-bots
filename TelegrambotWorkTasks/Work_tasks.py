from utils import create_bot, get_db_connection
from interaction import send_welcome
from database import check_and_create_tables
from database import execute_sql_query  # функция для выполнения SQL запросов.

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


@bot.message_handler(func=lambda message: True)
def entrance(message):
    print(f'Сообщение: {message}\n')

    user_id = str(message.from_user.id)
    username = message.from_user.username if message.from_user.username else None
    first_name = message.from_user.first_name if message.from_user.first_name else None
    last_name = message.from_user.last_name if message.from_user.last_name else None

    print(f'Вошел(а) в систему:\nid пользователя-{user_id}\nusername-{username}\n'
          f'first_name-{first_name}\nlast_name-{last_name}\n')

    # Проверяем, существует ли уже пользователь в базе данных
    query = "SELECT * FROM users WHERE id_user = %s::BIGINT"
    result = execute_sql_query(cnx, cursor, query, (user_id,))
    print(f"Запрос в бд:\n {result}")

    if not result:
        # Если пользователя нет, добавляем его в базу данных
        insert_query = """
            INSERT INTO users (id_user, first_name, last_name)
            VALUES (%s::BIGINT, %s, %s)
        """
        execute_sql_query(cnx, cursor, insert_query, (user_id, first_name, last_name))
        cnx.commit()
        print(f"Новый пользователь {first_name} {last_name} добавлен в базу данных.")
        # Отправляем сообщение пользователю
        send_welcome(message)
    else:
        print(f"Пользователь {first_name} {last_name} уже существует в базе данных.")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = str(call.chat.id)
    print(f'chat_id: {chat_id}')
    if call.data == 'knight':
        print("Водитель")
        user_id = str(call.from_user.id)
        username = call.from_user.username if call.from_user.username else None
        first_name = call.from_user.first_name if call.from_user.first_name else None
        last_name = call.from_user.last_name if call.from_user.last_name else None


        pass
        bot.send_message(call.message.chat.id, 'Введите имя и фамилию.')
        # print('Введите имя')
        # bot.register_next_step_handler(call.message, handle_first_name_input, users_data, chat_id)
    elif call.data == 'mouse':
        print("Мышь")
        bot.send_message(call.message.chat.id, 'Возвращайтесь если передумаете.')
        pass


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    finally:
        # Закрываем соединение с базой данных после завершения работы бота
        cursor.close()
        cnx.close()
