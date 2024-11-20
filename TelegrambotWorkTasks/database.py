import psycopg2
from database_connection import connect_to_database


def check_and_create_tables(cursor):
    """Проверяет наличие необходимых таблиц и создает их при необходимости."""
    tables_to_check = [
        ("users", """
            id_user BIGINT PRIMARY KEY, 
            first_name VARCHAR(100) NULL,
            last_name VARCHAR(100) NULL,
            username VARCHAR(100) NULL,
            user_status VARCHAR(100) NULL
        """),
        ("tasks", """
            id_task SERIAL PRIMARY KEY,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author INTEGER REFERENCES users(id_user) NOT NULL,
            city TEXT,
            address TEXT,
            task_text TEXT,
            task_status VARCHAR(100) NOT NULL,
            executor INTEGER REFERENCES users(id_user) NULL
        """)
    ]

    for table_name, columns in tables_to_check:
        cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='{table_name}')")
        has_table = cursor.fetchone()[0]

        if not has_table:
            print(f"Таблица {table_name} не найдена. Создание таблицы...")

            # Print the SQL statement to verify it looks correct
            print(cursor.mogrify(f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    {columns}
                )
            """))

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    {columns}
                )
            """)

            print(f"Таблица {table_name} создана.")

    print("Все необходимые таблицы созданы или уже существуют.\n")


def main():
    """Основная функция программы.
    Устанавливает соединение с базой данных,
    проверяет наличие и создает необходимые таблицы,
    выполняет операции с базой данных,
    а затем закрывает соединение."""
    cnx = connect_to_database()
    if cnx:
        cursor = cnx.cursor()

        # Проверяем наличие и создаем таблицы при необходимости
        check_and_create_tables(cursor)

        cnx.commit()
        cursor.close()
        cnx.close()
    else:
        print("Не удалось установить соединение с базой данных.")


def execute_sql_query(cnx, cursor, query, params=None):
    """
    Выполняет SQL-запрос и возвращает результат.

    Аргументы:
        cnx (connection): Соединение с базой данных
        cursor (cursor): Курсор для выполнения запросов
        query (str): Текст SQL-запроса
        params (tuple или dict, опционально): Параметры для подстановки в запрос

    Возвращаемое значение:
        list или None: Результат выполнения запроса или None в случае ошибки

    Примечание:
        Функция автоматически фиксирует изменения (commit) при успешном выполнении запроса
        и откатывает транзакцию (rollback) в случае возникновения исключения.
    """
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        cnx.commit()
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка при выполнении SQL-запроса: {e}")
        cnx.rollback()
        return None


if __name__ == "__main__":
    main()
