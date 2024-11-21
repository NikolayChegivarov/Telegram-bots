from utils import create_bot, get_db_connection
from interaction import send_welcome, manager, driver
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
        return 'ok'
    else:
        print(f"Пользователь {first_name} {last_name} уже существует в базе данных.")
        manager(message)
        return 'ok'


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = int(call.from_user.id)
    print(f'chat_id: {user_id}')

    if call.data == 'knight':
        print("Родился водитель")
        user_status = "Водитель"

        update_query = """
            UPDATE users
            SET user_status = %s
            WHERE id_user = %s
        """

        result = execute_sql_query(cnx, cursor, update_query, (user_status, user_id))
        cnx.commit()

        print(f"Статус {call.from_user.first_name} обновлен.\n")

        # Отправить сообщение с просьбой указать имя и зарегистрировать обработчика следующего шага
        bot.send_message(call.message.chat.id, 'Введите имя.')
        return bot.register_next_step_handler_by_chat_id(call.message.chat.id, first_name_we_get)

    elif call.data == 'mouse':
        print("Мышь")
        bot.send_message(call.message.chat.id, 'Возвращайтесь если передумаете.')
        pass


def first_name_we_get(message):
    user_id = message.from_user.id
    first_name = message.text
    print(f"first_name: {first_name}")

    # Заносим имя в бд.
    update_query = """
        UPDATE users
        SET first_name = %s
        WHERE id_user = %s
    """

    result = execute_sql_query(cnx, cursor, update_query, (first_name, user_id))
    cnx.commit()

    print(f"Имя {first_name} в бд занесено.")

    bot.send_message(message.chat.id, 'Введите фамилию.')
    return bot.register_next_step_handler_by_chat_id(message.chat.id, last_name_we_get)


def last_name_we_get(message):
    user_id = message.from_user.id
    last_name = message.text
    print(f"last_name: {last_name}")

    # Заносим имя в бд.
    update_query = """
        UPDATE users
        SET last_name = %s
        WHERE id_user = %s
    """

    result = execute_sql_query(cnx, cursor, update_query, (last_name, user_id))
    cnx.commit()

    # Высылаем начальную клавиатуру для водителя.
    driver(message)

    print(f"Фамилия {last_name} в бд занесена.")


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    finally:
        # Закрываем соединение с базой данных после завершения работы бота
        cursor.close()
        cnx.close()
