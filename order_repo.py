from db_manager import DBManager

class OrderRepository:
    """
    Репозиторій для управління замовленнями в базі даних.
    """

    def create_order(self, user_id, phone_number, order_list, total_price, location):
        """
        Створює нове замовлення.
        Параметри:
            user_id (int): ID користувача.
            phone_number (str): Телефонний номер користувача.
            order_list (list): Список замовлених товарів.
            total_price (float): Загальна вартість замовлення.
            location (str): Місцезнаходження доставки.
        Повертає:
            int: ID створеного замовлення.
        """
        cnx = DBManager.get_connection(operation_type='write')
        cursor = cnx.cursor()
        cursor.execute("SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1;")
        order_id = cursor.fetchall()[0][0] + 1

        cursor.execute("INSERT INTO orders (order_id, user_id, phone_number, order_list, total_price, order_time, location, status) VALUES (%s, %s, %s, %s, %s, NOW(), %s, 'On Hold')",
                       (order_id, user_id, phone_number, str(order_list), total_price, location))
        cnx.commit()
        cursor.close()
        cnx.close()
        return order_id

    def get_last_order_id(self):
        """
        Отримує ID останнього замовлення.
        Повертає:
            int: Останній ID замовлення, або 0, якщо замовлень немає.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT MAX(order_id) FROM orders")
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        return int(result[0]) if result[0] is not None else 0

    def fetch_new_orders(self, last_order_id):
        """
        Отримує нові замовлення, що були створені після вказаного ID.
        Параметри:
            last_order_id (int): ID замовлення, починаючи з якого потрібно отримувати нові.
        Повертає:
            list[tuple]: Список нових замовлень.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT order_id, order_time FROM orders WHERE order_id > %s", (last_order_id,))
        new_orders = cursor.fetchall()
        cursor.close()
        cnx.close()
        return new_orders

    def get_active_orders(self):
        """
        Отримує список активних замовлень.
        Повертає:
            list[tuple]: Список активних замовлень з ID і статусом.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT order_id, status FROM orders WHERE status IN ('On Hold', 'In Progress', 'Delivery')")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def get_orders_today(self):
        """
        Отримує список замовлень за сьогодні.
        Повертає:
            list[tuple]: Список замовлень, зроблених сьогодні, включаючи ID замовлення та статус.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT order_id, status FROM orders WHERE DATE(order_time) = CURDATE()")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def get_orders_last_week(self):
        """
        Отримує список замовлень за останній тиждень.
        Повертає:
            list[tuple]: Список замовлень за останній тиждень, включаючи ID замовлення та статус.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT order_id, status FROM orders WHERE order_time >= CURDATE() - INTERVAL 7 DAY")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def get_orders_last_month(self):
        """
        Отримує список замовлень за останній місяць.
        Повертає:
            list[tuple]: Список замовлень за останній місяць.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_time >= CURDATE() - INTERVAL 1 MONTH")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def get_orders_last_year(self):
        """
        Отримує список замовлень за останній рік.
        Повертає:
            list[tuple]: Список замовлень за останній рік.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_time >= CURDATE() - INTERVAL 1 YEAR")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def get_all_orders(self):
        """
        Отримує список усіх замовлень.
        Повертає:
            list[tuple]: Список усіх замовлень.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def get_order_details(self, order_id):
        """
        Отримує деталі конкретного замовлення.
        Параметри:
            order_id (int): ID замовлення.
        Повертає:
            list[tuple]: Деталі замовлення.
        """
        cnx = DBManager.get_connection(operation_type='read')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def change_order_status(self, order_id, status):
        """
        Змінює статус замовлення.
        Параметри:
            order_id (int): ID замовлення.
            status (str): Новий статус замовлення.
        """
        cnx = DBManager.get_connection(operation_type='write')
        cursor = cnx.cursor()
        cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (status, order_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
