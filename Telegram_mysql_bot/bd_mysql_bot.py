import os
import json
from connection_check import check_database_connection
from activ_db_check import activ_check
from convert import convert_phone, limit_text
from database_connection import *
from interaction import send_welcome
from change_wait_timeout import update_wait_timeout


# Подключение.
bot = telebot.TeleBot(TELEGRAM_TOKEN)
cnx, cursor = connect_to_database()


# Проверяем, подключились ли к базе данных
check_database_connection(cnx)
# Проверяем активную базу данных
activ_check(cursor)

# Обновляем максимальное время ожидания для текущей сессии.
update_wait_timeout(cursor)

# Используем словарь для хранения данных пользователей
users_data = {}


# Функция обратного вызова для обработки всех входящих сообщений
@bot.message_handler(func=lambda message: True)  # True означает, что обработчик будет применяться ко всем сообщениям.
def entrance(message):
    print(f'Сообщение: {message}')
    print(f'{message.from_user.first_name} вошел в систему.')

    # Инициализация данных пользователя
    chat_id = str(message.chat.id)
    users_data[chat_id] = {'first_last_name': '', 'phone': '', 'spec': '', 'about': '', 'photo': ''}
    print(f'Завели пользователя в переменную {users_data}.')

    # Отправка приветственного сообщения и кнопок
    send_welcome(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = str(call.message.chat.id)
    print(f'Завели пользователя в переменную2 {users_data}.')
    if call.data == 'register':
        bot.send_message(call.message.chat.id, 'Введите имя и фамилию.')  # message.chat.id,
        print('Введите имя')
        bot.register_next_step_handler(call.message, handle_first_name_input, users_data, chat_id)
    elif call.data == 'no':
        print(users_data)
        pass


def handle_first_name_input(message, users_data, chat_id):
    try:
        users_data[chat_id]['first_last_name'] = message.text
        print('Сохранили имя.')
        bot.send_message(message.chat.id, 'Введите номер телефона без кода страны.')
        print('Введите телефон.')
        bot.register_next_step_handler(message, handle_phone_input, users_data, chat_id)
    except KeyError:
        print(f"User ID {chat_id} not found in user_data.")


def handle_phone_input(message, users_data, chat_id):
    users_data[chat_id]['phone'] = convert_phone(message.text)  # Конвертируем номер.
    print('Сохранили телефон.')
    bot.send_message(message.chat.id, 'Введите свою специальность.')
    print('Введите спец.')
    bot.register_next_step_handler(message, handle_spec_input, users_data, chat_id)


def handle_spec_input(message, users_data, chat_id):
    users_data[chat_id]['spec'] = message.text
    print('Сохранили спец.')
    bot.send_message(message.chat.id, 'Расскажите о себе (2-3 предложения).')
    print('Расскажите о себе.')
    bot.register_next_step_handler(message, handle_about_input, users_data, chat_id)


def handle_about_input(message, users_data, chat_id):
    users_data[chat_id]['about'] = limit_text(message.text)
    print('Сохранили о себе.')
    bot.send_message(message.chat.id, 'Пожалуйста, отправьте ваше фото.')
    print('Запросили фото.')
    bot.register_next_step_handler(message, handle_photo_input, users_data, chat_id)


def handle_photo_input(message, users_data, chat_id):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Убедитесь, что директория фотографий существует
    if not os.path.exists("photos"):
        os.makedirs("photos")

    # Помещаем в user_data
    with open(f"photos/{chat_id}.jpg", "wb") as new_file:
        new_file.write(downloaded_file)
    users_data[chat_id]['photo'] = f"photos/{chat_id}.jpg"
    # id_user = send_farewell(message)

    # Преобразование user_data в словарь Python
    python_dict = dict(users_data)

    # Преобразование словаря Python в JSON-строку перед отправкой
    user_data_json = json.dumps(python_dict, ensure_ascii=False, indent=4)
    bot.send_message(message.chat.id, user_data_json)
    print(f"Собранная информация: {users_data}")

    # Начинаем транзакцию
    cnx.start_transaction()

    # Вставка имени в wp_posts
    sql = 'INSERT INTO wp_posts (post_title) VALUES(%s)'
    val = (users_data[chat_id]['first_last_name'],)
    cursor.execute(sql, val)
    print('Имя записано')

    # Получаем ID последней вставленной строки
    id_post = cursor.lastrowid

    print(f'ID поста: {id_post}')

    sql = 'INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(%s, %s, %s)'  # Куда закачиваем.
    val = (id_post, 'master_tel', users_data[chat_id]['phone'])  # То что закачиваем
    cursor.execute(sql, val)

    sql = 'INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(%s, %s, %s)'
    val = (id_post, 'master_spec', users_data[chat_id]['spec'])
    cursor.execute(sql, val)

    sql = 'INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES(%s, %s, %s)'
    val = (id_post, 'master_about', users_data[chat_id]['about'])
    cursor.execute(sql, val)

    # Завершаем транзакцию и сохраняем изменения
    cnx.commit()

    # bot.send_message(message.chat.id, 'Вы успешно зарегистированны')  # Corrected here
    print('user создан В БАЗЕ ДАННЫХ')

    users_data.pop(chat_id)
    print('ИНФОРМАЦИЯ СТЕРТА')
    print()


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
if __name__ == '__main__':
    bot.polling(none_stop=True)
