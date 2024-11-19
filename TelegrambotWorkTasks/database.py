import psycopg2
from database_connection import connect_to_database


def check_and_create_tables(cursor):
    """Проверяет наличие необходимых таблиц и создает их при необходимости."""
    tables_to_check = [
        ("users", """
            id_user INTEGER PRIMARY KEY, 
            name VARCHAR(100) NOT NULL,
            surname VARCHAR(100) NOT NULL,
            user_status VARCHAR(100) NOT NULL
        """),
        ("tasks", """
            id_task SERIAL PRIMARY KEY,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            avtor INTEGER REFERENCES users(id_user) NOT NULL,
            address TEXT,
            task_text TEXT,
            task_status VARCHAR(100) NOT NULL,
            driver INTEGER REFERENCES users(id_user) NULL
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

    print("Все необходимые таблицы созданы или уже существуют.")


def main():
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


if __name__ == "__main__":
    main()
