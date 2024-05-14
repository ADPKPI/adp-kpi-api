from db_manager import DBManager

class MenuRepository:
    """
    Репозиторій для управління меню в базі даних.
    """

    def get_menu(self):
        """
        Отримує список усіх страв з меню.
        Повертає:
            list[tuple]: Список назв страв.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT name FROM menu")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def get_pizza_details(self, pizza_name):
        """
        Отримує деталі піци за назвою.
        Параметри:
            pizza_name (str): Назва піци, деталі якої потрібно отримати.
        Повертає:
            tuple: Деталі піци, включаючи назву, опис, посилання на фото, ціну та ID.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT name, description, photo_url, price, id FROM menu WHERE name = %s", (pizza_name,))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()
        return row

    def get_pizza_details_by_id(self, product_id):
        """
        Отримує деталі піци за ID продукту.
        Параметри:
            product_id (int): ID продукту, деталі якого потрібно отримати.
        Повертає:
            tuple: Деталі піци, включаючи ID, назву та ціну.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT id, name, price FROM menu WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()
        return row
