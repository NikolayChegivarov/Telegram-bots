from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:
    """
    Класс для создания клавиатуры регистрации с различными опциями выбора задач.

    Атрибуты:
    - markup (InlineKeyboardMarkup): Объект клавиатуры с настроенной шириной строки.
    - button_kostroma (InlineKeyboardButton): Кнопка для выбора задач Костромы.
    - button_msk (InlineKeyboardButton): Кнопка для выбора задач Москвы.
    - button_full (InlineKeyboardButton): Кнопка для выбора всех задач.
    - button_set (InlineKeyboardButton): Кнопка для постановки новой задачи.
    - button_del (InlineKeyboardButton): Кнопка для удаления задачи.

    Методы:
    - __init__(): Инициализация объекта клавиатуры с созданием кнопок.
    - get_markup(): Добавление кнопок на клавиатуру и возврат готовой разметки.
    """
    def __init__(self):
        """
        Инициализация объекта клавиатуры с созданием кнопок.

        Создает экземпляр InlineKeyboardMarkup и определяет различные кнопки выбора задач.
        """
        self.markup = InlineKeyboardMarkup(row_width=2)
        self.button_knight = InlineKeyboardButton('Рыцарь дорог', callback_data='knight')
        self.button_mouse = InlineKeyboardButton('Мышь офисная', callback_data='mouse')
        self.button_kostroma = InlineKeyboardButton('Задачи сегодня Кострома', callback_data='kostroma')
        self.button_msk = InlineKeyboardButton('Задачи сегодня Москва', callback_data='msk')
        self.button_full = InlineKeyboardButton('Задачи все', callback_data='full')
        self.button_set = InlineKeyboardButton('Поставить задачу', callback_data='set')
        self.button_del = InlineKeyboardButton('Удалить задачу', callback_data='del')
        self.button_no = InlineKeyboardButton('Взять задачу', callback_data='take')
        self.button_no = InlineKeyboardButton('Пометить "сделано"', callback_data='done')

    def registration(self):
        """
        Добавление кнопок на клавиатуру и возврат готовой разметки.
        """
        self.markup.add(self.button_knight, self.button_mouse)
        print('Предложили выбор кнопок.')
        return self.markup

    # def registration(self):
    #     """
    #     Добавление кнопок на клавиатуру и возврат готовой разметки.
    #     """
    #     self.markup.add(self.button_kostroma, self.button_msk, self.button_full, self.button_set, self.button_del)
    #     print('Предложили выбор кнопок.')
    #     return self.markup
