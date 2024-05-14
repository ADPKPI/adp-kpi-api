from flask import Flask, request, jsonify, abort
from menu_repo import MenuRepository
from order_repo import OrderRepository
from user_repo import UserRepository
from cart_repo import CartRepository
from db_manager import DBManager
from config import DB_CONFIG

app = Flask(__name__)

@app.route('/menu', methods=['GET'])
def get_menu():
    """
    Отримує повний список меню.
    Повертає:
        json: Список усіх страв у меню.
    """
    try:
        menu_items = MenuRepository().get_menu()
        return jsonify(menu_items)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/menu/details/<pizza_name>', methods=['GET'])
def get_pizza_details(pizza_name):
    """
    Отримує деталі піци за назвою.
    Аргументи:
        pizza_name (str): Назва піци, деталі якої потрібно отримати.
    Повертає:
        json: Деталі піци, або помилку 404, якщо піцу не знайдено.
    """
    try:
        pizza_details = MenuRepository().get_pizza_details(pizza_name)
        if pizza_details:
            return jsonify(pizza_details)
        else:
            abort(404, description="Pizza not found")
    except Exception as e:
        abort(500, description=str(e))

@app.route('/menu/details-by-id/<int:product_id>', methods=['GET'])
def get_pizza_details_by_id(product_id):
    """
    Отримує деталі піци за ID продукту.
    Аргументи:
        product_id (int): ID продукту, деталі якого потрібно отримати.
    Повертає:
        json: Деталі піци, або помилку 404, якщо піцу не знайдено.
    """
    try:
        pizza_details = MenuRepository().get_pizza_details_by_id(product_id)
        if pizza_details:
            return jsonify(pizza_details)
        else:
            abort(404, description="Product not found")
    except Exception as e:
        abort(500, description=str(e))

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """
    Додає продукт в корзину користувача.
    Параметри:
        user_id (int): ID користувача.
        product_id (int): ID продукту, що додається.
    Повертає:
        json: Повідомлення про успішне додавання.
    """
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    try:
        CartRepository().add_to_cart(user_id, product_id)
        return jsonify({'message': 'Product added to cart'})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """
    Отримує список усіх товарів у корзині користувача.
    Параметри:
        user_id (int): ID користувача.
    Повертає:
        json: Список товарів у корзині.
    """
    try:
        cart_items = CartRepository().get_cart(user_id)
        return jsonify(cart_items)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/cart/clear/<int:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    """
    Очищує корзину користувача.
    Параметри:
        user_id (int): ID користувача.
    Повертає:
        json: Повідомлення про очищення корзини.
    """
    try:
        CartRepository().clear_cart(user_id)
        return jsonify({'message': 'Cart cleared'})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Отримує інформацію про користувача.
    Параметри:
        user_id (int): ID користувача.
    Повертає:
        json: Деталі користувача.
    """
    try:
        user_details = UserRepository().get_user(user_id)
        return jsonify(user_details)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/user/add', methods=['POST'])
def add_user():
    """
    Додає нового користувача в систему.
    Параметри:
        user_id (int): ID нового користувача.
        username (str): Ім'я користувача.
        firstname (str): Ім'я.
        lastname (str): Прізвище.
    Повертає:
        json: Повідомлення про додавання користувача.
    """
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    try:
        UserRepository().add_user(user_id, username, firstname, lastname)
        return jsonify({'message': 'User added'})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/user/update/contact', methods=['PATCH'])
def update_user_contact():
    """
    Оновлює контактні дані користувача.
    Параметри:
        user_id (int): ID користувача.
        phone_number (str): Номер телефону.
        location (str): Місцезнаходження.
    Повертає:
        json: Повідомлення про оновлення контактів.
    """
    data = request.json
    user_id = data.get('user_id')
    phone_number = data.get('phone_number')
    location = data.get('location')
    try:
        UserRepository().update_user_contact(user_id, phone_number, location)
        return jsonify({'message': 'User contact updated'})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/order/create', methods=['POST'])
def create_order():
    """
    Створює нове замовлення.
    Параметри:
        user_id (int): ID користувача, який робить замовлення.
        phone_number (str): Телефонний номер користувача.
        order_list (list): Список замовлених товарів.
        total_price (float): Загальна вартість замовлення.
        location (str): Адреса доставки.
    Повертає:
        json: ID створеного замовлення.
    """
    data = request.json
    user_id = data.get('user_id')
    phone_number = data.get('phone_number')
    order_list = data.get('order_list')
    total_price = data.get('total_price')
    location = data.get('location')
    try:
        order_id = OrderRepository().create_order(user_id, phone_number, order_list, total_price, location)
        return jsonify({'order_id': order_id})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/active', methods=['GET'])
def get_active_orders():
    """
    Отримує список активних замовлень.
    Повертає:
        json: Список активних замовлень.
    """
    try:
        orders = OrderRepository().get_active_orders()
        return jsonify(orders)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/today', methods=['GET'])
def get_orders_today():
    """
    Отримує список замовлень зроблених сьогодні.
    Повертає:
        json: Список замовлень зроблених сьогодні.
    """
    try:
        orders = OrderRepository().get_orders_today()
        return jsonify(orders)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/last-week', methods=['GET'])
def get_orders_last_week():
    """
    Отримує список замовлень за останній тиждень.
    Повертає:
        json: Список замовлень за останній тиждень.
    """
    try:
        orders = OrderRepository().get_orders_last_week()
        return jsonify(orders)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/last-month', methods=['GET'])
def get_orders_last_month():
    """
    Отримує список замовлень за останній місяць.
    Повертає:
        json: Список замовлень за останній місяць.
    """
    try:
        orders = OrderRepository().get_orders_last_month()
        return jsonify(orders)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/last-year', methods=['GET'])
def get_orders_last_year():
    """
    Отримує список замовлень за останній рік.
    Повертає:
        json: Список замовлень за останній рік.
    """
    try:
        orders = OrderRepository().get_orders_last_year()
        return jsonify(orders)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/all', methods=['GET'])
def get_all_orders():
    """
    Отримує список всіх замовлень.
    Повертає:
        json: Список всіх замовлень.
    """
    try:
        orders = OrderRepository().get_all_orders()
        return jsonify(orders)
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/details/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    """
    Отримує деталі конкретного замовлення.
    Параметри:
        order_id (int): ID замовлення.
    Повертає:
        json: Деталі замовлення або помилку 404, якщо замовлення не знайдено.
    """
    try:
        order_details = OrderRepository().get_order_details(order_id)
        if order_details:
            return jsonify(order_details)
        else:
            abort(404, description="Order not found")
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/change-status', methods=['PATCH'])
def change_order_status():
    """
    Оновлює статус замовлення.
    Параметри:
        order_id (int): ID замовлення, статус якого потрібно оновити.
        status (str): Новий статус замовлення.
    Повертає:
        json: Повідомлення про оновлення статусу замовлення.
    """
    data = request.json
    order_id = data.get('order_id')
    status = data.get('status')
    if not order_id or not status:
        abort(400, description="Missing order_id or status")
    try:
        OrderRepository().change_order_status(order_id, status)
        return jsonify({'message': f'Order {order_id} status updated to {status}'})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/last-order-id', methods=['GET'])
def get_last_order_id():
    """
    Отримує ID останнього замовлення.
    Повертає:
        json: ID останнього замовлення.
    """
    try:
        last_order_id = OrderRepository().get_last_order_id()
        return jsonify({'last_order_id': last_order_id})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/orders/fetch-new/<int:last_order_id>', methods=['GET'])
def fetch_new_orders(last_order_id):
    """
    Отримує нові замовлення, починаючи від вказаного ID.
    Параметри:
        last_order_id (int): ID, починаючи з якого потрібно отримувати нові замовлення.
    Повертає:
        json: Список нових замовлень.
    """
    try:
        new_orders = OrderRepository().fetch_new_orders(last_order_id)
        return jsonify(new_orders)
    except Exception as e:
        abort(500, description=str(e))


if __name__ == '__main__':
    db = DBManager(DB_CONFIG)
    app.run(host='206.54.191.53', port=5000)
