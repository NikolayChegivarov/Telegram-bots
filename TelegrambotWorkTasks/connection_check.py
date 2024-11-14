from psycopg2 import OperationalError


def check_database_connection(db_connection):
    """
    Проверяет подключение к базе данных.

    Args:
    db_connection (psycopg2 connection): Объект соединения с базой данных.

    Returns:
    bool: True, если подключение установлено успешно; False в противном случае.

    Raises:
    OperationalError: При возникновении ошибок операционной работы с базой данных.
    """
    try:
        db_connection.cursor().execute("SELECT 1")
        print("Подключение к базе данных установлено.")
        return True
    except OperationalError:
        print("Не удалось подключиться к базе данных.")
        return False
