from db_manager import DBManager

class UserRepository:
    """
    Репозиторій для управління інформацією про користувачів у базі даних.
    """

    def get_user(self, user_id):
        """
        Отримує інформацію про користувача за його ID.
        Параметри:
            user_id (int): ID користувача.
        Повертає:
            tuple: Інформація про користувача або None, якщо користувача не знайдено.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()
        return row

    def add_user(self, user_id, username, firstname, lastname):
        """
        Додає нового користувача в базу даних.
        Параметри:
            user_id (int): ID користувача.
            username (str): Ім'я користувача.
            firstname (str): Ім'я.
            lastname (str): Прізвище.
        """
        cnx = DBManager.get_connection(operation_type='write')
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO users (user_id, username, firstname, lastname) VALUES (%s, %s, %s, %s)",
                       (user_id, username, firstname, lastname))
        cnx.commit()
        cursor.close()
        cnx.close()

    def update_user_contact(self, user_id, phone_number=None, location=None):
        """
        Оновлює контактну інформацію користувача.
        Параметри:
            user_id (int): ID користувача.
            phone_number (str, optional): Новий телефонний номер.
            location (str, optional): Нове місцеперебування.
        """
        cnx = DBManager.get_connection(operation_type='write')
        cursor = cnx.cursor()
        if phone_number:
            cursor.execute("UPDATE users SET phone_number=%s WHERE user_id = %s", (phone_number, user_id))
        if location:
            cursor.execute("UPDATE users SET saved_location=%s WHERE user_id = %s", (location, user_id))
        cnx.commit()
        cursor.close()
        cnx.close()
