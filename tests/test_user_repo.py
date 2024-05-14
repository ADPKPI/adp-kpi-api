import pytest
from unittest.mock import MagicMock, patch
from user_repo import UserRepository


@patch('user_repo.DBManager.get_connection')
def test_get_user(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, 'test_user', 'Test', 'User', '123456789', 'Location')

    repo = UserRepository()
    result = repo.get_user(1)

    mock_get_connection.assert_called_once_with(operation_type='read')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE user_id = %s", (1,))
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    assert result == (1, 'test_user', 'Test', 'User', '123456789', 'Location')


@patch('user_repo.DBManager.get_connection')
def test_add_user(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor

    repo = UserRepository()
    repo.add_user(1, 'test_user', 'Test', 'User')

    mock_get_connection.assert_called_once_with(operation_type='write')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (user_id, username, firstname, lastname) VALUES (%s, %s, %s, %s)",
        (1, 'test_user', 'Test', 'User')
    )
    mock_cnx.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()


@patch('user_repo.DBManager.get_connection')
def test_update_user_contact(mock_get_connection):
    mock_cnx = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_cnx
    mock_cnx.cursor.return_value = mock_cursor

    repo = UserRepository()
    repo.update_user_contact(1, phone_number='123456789')

    mock_get_connection.assert_called_once_with(operation_type='write')
    mock_cnx.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "UPDATE users SET phone_number=%s WHERE user_id = %s", ('123456789', 1)
    )
    mock_cnx.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_cnx.close.assert_called_once()

    repo.update_user_contact(1, location='New Location')

    mock_cursor.execute.assert_called_with(
        "UPDATE users SET saved_location=%s WHERE user_id = %s", ('New Location', 1)
    )
    mock_cnx.commit.assert_called()


if __name__ == "__main__":
    pytest.main()
