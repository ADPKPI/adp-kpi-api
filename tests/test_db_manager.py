import pytest
from unittest.mock import patch, MagicMock
from mysql.connector import pooling
from db_manager import DBManager

@patch('db_manager.pooling.MySQLConnectionPool')
def test_init(mock_mysql_pool):
    config = {
        'master': {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'},
        'slaves': [
            {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'},
            {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'}
        ]
    }

    DBManager.__init__(config)

    assert mock_mysql_pool.call_count == 3
    mock_mysql_pool.assert_any_call(pool_name="master-pool", pool_size=5, **config['master'])
    for i, slave_config in enumerate(config['slaves']):
        mock_mysql_pool.assert_any_call(pool_name=f"slave-pool-{i}", pool_size=5, **slave_config)

@patch('db_manager.pooling.MySQLConnectionPool')
def test_get_connection_write(mock_mysql_pool):
    mock_master_pool = MagicMock()
    mock_mysql_pool.return_value = mock_master_pool
    config = {
        'master': {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'},
        'slaves': []
    }
    DBManager.__init__(config)
    connection = DBManager.get_connection(operation_type='write')
    mock_master_pool.get_connection.assert_called_once()
    assert connection == mock_master_pool.get_connection.return_value

@patch('db_manager.pooling.MySQLConnectionPool')
def test_get_connection_read(mock_mysql_pool):
    mock_slave_pool_1 = MagicMock()
    mock_slave_pool_2 = MagicMock()
    mock_mysql_pool.side_effect = [MagicMock(), mock_slave_pool_1, mock_slave_pool_2]
    config = {
        'master': {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'},
        'slaves': [
            {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'},
            {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'}
        ]
    }
    DBManager.__init__(config)

    connection = DBManager.get_connection(operation_type='read')
    mock_slave_pool_1.get_connection.assert_called_once()
    assert connection == mock_slave_pool_1.get_connection.return_value

    connection = DBManager.get_connection(operation_type='read')
    mock_slave_pool_2.get_connection.assert_called_once()
    assert connection == mock_slave_pool_2.get_connection.return_value

@patch('db_manager.pooling.MySQLConnectionPool')
def test_get_connection_fallback_to_master(mock_mysql_pool):
    mock_master_pool = MagicMock()
    mock_slave_pool_1 = MagicMock()
    mock_slave_pool_2 = MagicMock()
    mock_slave_pool_1.get_connection.side_effect = Exception("Slave 1 down")
    mock_slave_pool_2.get_connection.side_effect = Exception("Slave 2 down")
    mock_mysql_pool.side_effect = [mock_master_pool, mock_slave_pool_1, mock_slave_pool_2]
    config = {
        'master': {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'},
        'slaves': [
            {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'},
            {'user': 'test', 'password': 'test', 'host': '127.0.0.1', 'database': 'test_db'}
        ]
    }
    DBManager.__init__(config)

    connection = DBManager.get_connection(operation_type='read')
    mock_slave_pool_1.get_connection.assert_called_once()
    mock_slave_pool_2.get_connection.assert_called_once()
    mock_master_pool.get_connection.assert_called_once()
    assert connection == mock_master_pool.get_connection.return_value

if __name__ == "__main__":
    pytest.main()
