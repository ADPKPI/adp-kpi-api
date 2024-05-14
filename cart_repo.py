from db_manager import DBManager
from menu_repo import MenuRepository

class CartRepository:
    """
    Репозиторій для управління кошиком користувачів у базі даних.
    """

    def add_to_cart(self, user_id, product_id):
        """
        Додає продукт до кошика користувача або збільшує кількість, якщо продукт вже є в кошику.
        Параметри:
            user_id (int): ID користувача.
            product_id (int): ID продукту, який додається до кошика.
        """
        cnx = DBManager.get_connection(operation_type='write')
        cursor = cnx.cursor()
        cursor.execute("SELECT quantity, total_price FROM user_cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        cart_row = cursor.fetchone()

        if cart_row:
            new_quantity = cart_row[0] + 1
            new_total_price = new_quantity * (cart_row[1]/cart_row[0])
            cursor.execute("UPDATE user_cart SET quantity = %s, total_price = %s WHERE user_id = %s AND product_id = %s",
                           (new_quantity, new_total_price, user_id, product_id))
        else:
            menu_row = MenuRepository().get_pizza_details_by_id(product_id)
            if menu_row:
                cursor.execute(
                    "INSERT INTO user_cart (user_id, product_id, product_name, quantity, total_price) VALUES (%s, %s, %s, 1, %s)",
                    (user_id, product_id, menu_row[1], menu_row[2]))
        cnx.commit()
        cursor.close()
        cnx.close()

    def get_cart(self, user_id):
        """
        Отримує всі продукти в кошику користувача.
        Параметри:
            user_id (int): ID користувача.
        Повертає:
            list[tuple]: Список продуктів у кошику з назвою, кількістю і загальною вартістю.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT product_name, quantity, total_price FROM user_cart WHERE user_id = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def clear_cart(self, user_id):
        """
        Видаляє всі продукти з кошика користувача.
        Параметри:
            user_id (int): ID користувача.
        """
        cnx = DBManager.get_connection(operation_type='write')
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM user_cart WHERE user_id = %s", (user_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
