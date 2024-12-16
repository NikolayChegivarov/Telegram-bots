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
        self.button_tasks_all = InlineKeyboardButton('Просмотр задач', callback_data='tasks')
        self.button_task_kostroma = InlineKeyboardButton('Задачи сегодня Кострома', callback_data='kostroma')
        self.button_task_msk = InlineKeyboardButton('Задачи сегодня Москва', callback_data='msk')
        self.button_task_nn = InlineKeyboardButton('Задачи сегодня Нижний Новгород', callback_data='nn')
        self.button_task_rf = InlineKeyboardButton('Прочие города', callback_data='rf')
        # Кнопки менеджерам.
        self.button_set_a_task = InlineKeyboardButton('Поставить задачу', callback_data='set')
        self.button_del = InlineKeyboardButton('Удалить задачу', callback_data='del')
        # Кнопки водителям.
        self.button_no = InlineKeyboardButton('Взять задачу', callback_data='take')
        self.button_no = InlineKeyboardButton('Пометить "сделано"', callback_data='done')
        self.button_my_tasks = InlineKeyboardButton('Мои задачи', callback_data='my_tasks')

    def registration_keyboard(self):
        """
        Добавление кнопок на клавиатуру.
        """
        self.markup.add(self.button_knight, self.button_mouse)
        # print('Кнопки: Водитель или мышь?\n')
        return self.markup

    def manager_keyboard(self):
        """
        Клавиатура для менеджеров.
        """
        self.markup.add(self.button_tasks_all, self.button_set_a_task)
        return self.markup

    def driver_keyboard(self):
        """
        Клавиатура для водителей.
        """
        self.markup.add(self.button_tasks_all, self.button_my_tasks)
        return self.markup

    def tasks_keyboard(self):
        """
        Клавиатура задачи.
        """
        self.markup.add(self.button_task_kostroma, self.button_task_msk, self.button_task_nn)
        return self.markup
