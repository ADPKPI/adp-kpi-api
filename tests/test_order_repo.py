import pytest
from unittest.mock import MagicMock, patch
from order_repo import OrderRepository


@patch('order_repo.DBManager.get_connection')
def test_create_order(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(99,)]

    repo = OrderRepository()
    order_id = repo.create_order(1, '123456789', [('Pizza1', 2)], 20.0, 'Location')

    mock_get_connection.assert_called_once_with(operation_type='write')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call("SELECT order_id FROM orders ORDER BY order_id DESC LIMIT 1;")
    mock_cursor.execute.assert_any_call(
        "INSERT INTO orders (order_id, user_id, phone_number, order_list, total_price, order_time, location, status) VALUES (%s, %s, %s, %s, %s, NOW(), %s, 'On Hold')",
        (100, 1, '123456789', str([('Pizza1', 2)]), 20.0, 'Location')
    )
    mock_cnx.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert order_id == 100


@patch('order_repo.DBManager.get_connection')
def test_get_last_order_id(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (100,)

    repo = OrderRepository()
    last_order_id = repo.get_last_order_id()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT MAX(order_id) FROM orders")
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert last_order_id == 100


@patch('order_repo.DBManager.get_connection')
def test_fetch_new_orders(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(101, '2024-01-01 10:00:00'), (102, '2024-01-01 11:00:00')]

    repo = OrderRepository()
    new_orders = repo.fetch_new_orders(100)

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT order_id, order_time FROM orders WHERE order_id > %s", (100,))
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert new_orders == [(101, '2024-01-01 10:00:00'), (102, '2024-01-01 11:00:00')]


@patch('order_repo.DBManager.get_connection')
def test_get_active_orders(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(101, 'On Hold'), (102, 'In Progress')]

    repo = OrderRepository()
    active_orders = repo.get_active_orders()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT order_id, status FROM orders WHERE status IN ('On Hold', 'In Progress', 'Delivery')")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert active_orders == [(101, 'On Hold'), (102, 'In Progress')]


@patch('order_repo.DBManager.get_connection')
def test_get_orders_today(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(101, 'On Hold'), (102, 'In Progress')]

    repo = OrderRepository()
    orders_today = repo.get_orders_today()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT order_id, status FROM orders WHERE DATE(order_time) = CURDATE()")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert orders_today == [(101, 'On Hold'), (102, 'In Progress')]


@patch('order_repo.DBManager.get_connection')
def test_get_orders_last_week(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(101, 'On Hold'), (102, 'In Progress')]

    repo = OrderRepository()
    orders_last_week = repo.get_orders_last_week()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT order_id, status FROM orders WHERE order_time >= CURDATE() - INTERVAL 7 DAY")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert orders_last_week == [(101, 'On Hold'), (102, 'In Progress')]


@patch('order_repo.DBManager.get_connection')
def test_get_orders_last_month(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(101, 'On Hold'), (102, 'In Progress')]

    repo = OrderRepository()
    orders_last_month = repo.get_orders_last_month()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM orders WHERE order_time >= CURDATE() - INTERVAL 1 MONTH")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert orders_last_month == [(101, 'On Hold'), (102, 'In Progress')]


@patch('order_repo.DBManager.get_connection')
def test_get_orders_last_year(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(101, 'On Hold'), (102, 'In Progress')]

    repo = OrderRepository()
    orders_last_year = repo.get_orders_last_year()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM orders WHERE order_time >= CURDATE() - INTERVAL 1 YEAR")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert orders_last_year == [(101, 'On Hold'), (102, 'In Progress')]


@patch('order_repo.DBManager.get_connection')
def test_get_all_orders(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(101, 'On Hold'), (102, 'In Progress')]

    repo = OrderRepository()
    all_orders = repo.get_all_orders()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM orders")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert all_orders == [(101, 'On Hold'), (102, 'In Progress')]


@patch('order_repo.DBManager.get_connection')
def test_get_order_details(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (101, 1, '123456789', '[(Pizza1, 2)]', 20.0, '2024-01-01 10:00:00', 'Location', 'On Hold')]

    repo = OrderRepository()
    order_details = repo.get_order_details(101)

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM orders WHERE order_id = %s", (101,))
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert order_details == [(101, 1, '123456789', '[(Pizza1, 2)]', 20.0, '2024-01-01 10:00:00', 'Location', 'On Hold')]


@patch('order_repo.DBManager.get_connection')
def test_change_order_status(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor

    repo = OrderRepository()
    repo.change_order_status(101, 'Delivered')

    mock_get_connection.assert_called_once_with(operation_type='write')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("UPDATE orders SET status = %s WHERE order_id = %s", ('Delivered', 101))
    mock_cnx.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()


if __name__ == "__main__":
    pytest.main()
