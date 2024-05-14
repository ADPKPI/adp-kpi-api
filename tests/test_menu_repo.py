import pytest
from unittest.mock import MagicMock, patch
from menu_repo import MenuRepository
from db_manager import DBManager


@patch('menu_repo.DBManager.get_connection')
def test_get_menu(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Pizza1',), ('Pizza2',)]

    repo = MenuRepository()
    result = repo.get_menu()

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT name FROM menu")
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert result == [('Pizza1',), ('Pizza2',)]


@patch('menu_repo.DBManager.get_connection')
def test_get_pizza_details(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ('Pizza1', 'Delicious cheese pizza', 'http://example.com/photo.jpg', 10.0, 1)

    repo = MenuRepository()
    result = repo.get_pizza_details('Pizza1')

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT name, description, photo_url, price, id FROM menu WHERE name = %s", ('Pizza1',))
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert result == ('Pizza1', 'Delicious cheese pizza', 'http://example.com/photo.jpg', 10.0, 1)


@patch('menu_repo.DBManager.get_connection')
def test_get_pizza_details_by_id(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, 'Pizza1', 10.0)

    repo = MenuRepository()
    result = repo.get_pizza_details_by_id(1)

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT id, name, price FROM menu WHERE id = %s", (1,))
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert result == (1, 'Pizza1', 10.0)


if __name__ == "__main__":
    pytest.main()
