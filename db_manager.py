from mysql.connector import pooling
import logging

class DBManager:
    """
    Керує пулами підключень до бази даних з одним мастером і декількома слейвами.
    """
    _pools = {}
    _slave_index = 0  # Для циклічного доступу до слейвів

    @classmethod
    def __init__(cls, config):
        """
        Ініціалізація пулів підключень.
        Параметри:
            config (dict): Конфігурація для пулів. Включає 'master' і 'slaves'.
        """
        # Ініціалізація мастер пула
        cls._pools['master'] = pooling.MySQLConnectionPool(pool_name="master-pool", pool_size=5, **config['master'])

        # Ініціалізація слейв пулів
        cls._pools['slaves'] = []
        for slave_config in config['slaves']:
            pool_name = f"slave-pool-{len(cls._pools['slaves'])}"
            slave_pool = pooling.MySQLConnectionPool(pool_name=pool_name, pool_size=5, **slave_config)
            cls._pools['slaves'].append(slave_pool)

    @classmethod
    def get_connection(cls, operation_type='read'):
        """
        Отримання підключення до бази даних.
        Параметри:
            operation_type (str): Тип операції ('read' або 'write'), який визначає, з якого пула отримувати підключення.
        Повертає:
            MySQLConnection: Підключення до бази даних.
        Виключення:
            Exception: Якщо не вдається підключитися до мастер-сервера.
        """
        if operation_type == 'read':
            return cls._get_slave_connection()

        # Спроба отримати підключення з мастер-сервера
        try:
            return cls._pools['master'].get_connection()
        except Exception as e:
            logging.error(f"Error connecting to master server: {e}")
            raise Exception("Master server is unavailable.")

    @classmethod
    def _get_slave_connection(cls):
        """
        Отримання підключення з одного зі слейв-пулів.
        Повертає:
            MySQLConnection: Підключення до бази даних.
        Виключення:
            Exception: Якщо всі слейви недоступні, спроба підключення до мастера.
        """
        start_index = cls._slave_index
        num_slaves = len(cls._pools['slaves'])

        for _ in range(num_slaves):
            try:
                connection = cls._pools['slaves'][cls._slave_index].get_connection()
                cls._slave_index = (cls._slave_index + 1) % num_slaves
                return connection
            except Exception as e:
                logging.error(f"Error connecting to slave server at index {cls._slave_index}: {e}")
                cls._slave_index = (cls._slave_index + 1) % num_slaves

        # Якщо всі слейви недоступні, спроба підключення до мастера
        logging.error("All slave servers unavailable, attempting to connect to master server.")
        return cls._pools['master'].get_connection()
