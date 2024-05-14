import pytest
from unittest.mock import MagicMock, patch
from cart_repo import CartRepository


@patch('cart_repo.DBManager.get_connection')
@patch('cart_repo.MenuRepository.get_pizza_details_by_id')
def test_add_to_cart_new_item(mock_get_pizza_details, mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_get_pizza_details.return_value = (1, 'Pizza1', 10.0)

    repo = CartRepository()
    repo.add_to_cart(1, 1)

    mock_get_connection.assert_called_once_with(operation_type='write')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call(
        "SELECT quantity, total_price FROM user_cart WHERE user_id = %s AND product_id = %s",
        (1, 1)
    )
    mock_cursor.execute.assert_any_call(
        "INSERT INTO user_cart (user_id, product_id, product_name, quantity, total_price) VALUES (%s, %s, %s, 1, %s)",
        (1, 1, 'Pizza1', 10.0)
    )
    mock_cnx.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()


@patch('cart_repo.DBManager.get_connection')
def test_add_to_cart_existing_item(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, 10.0)

    repo = CartRepository()
    repo.add_to_cart(1, 1)

    mock_get_connection.assert_called_once_with(operation_type='write')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call(
        "SELECT quantity, total_price FROM user_cart WHERE user_id = %s AND product_id = %s",
        (1, 1)
    )
    mock_cursor.execute.assert_any_call(
        "UPDATE user_cart SET quantity = %s, total_price = %s WHERE user_id = %s AND product_id = %s",
        (2, 20.0, 1, 1)
    )
    mock_cnx.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()


@patch('cart_repo.DBManager.get_connection')
def test_get_cart(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Pizza1', 2, 20.0), ('Pizza2', 1, 10.0)]

    repo = CartRepository()
    result = repo.get_cart(1)

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT product_name, quantity, total_price FROM user_cart WHERE user_id = %s", (1,)
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert result == [('Pizza1', 2, 20.0), ('Pizza2', 1, 10.0)]


@patch('cart_repo.DBManager.get_connection')
def test_clear_cart(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor

    repo = CartRepository()
    repo.clear_cart(1)

    mock_get_connection.assert_called_once_with(operation_type='write')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM user_cart WHERE user_id = %s", (1,)
    )
    mock_cnx.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()


if __name__ == "__main__":
    pytest.main()
