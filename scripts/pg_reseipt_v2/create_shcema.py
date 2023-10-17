from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
#https://chat.openai.com/share/d7584faa-d19a-43c8-87ef-53c2f79c80f3
# Подключение к Cassandra

cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()

# Создание ключевого пространства
session.execute("""
CREATE KEYSPACE IF NOT EXISTS pgs_receipt 
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
""")
session.set_keyspace('pgs_receipt')

# Создание таблицы
# Создание таблицы с новыми колонками и изменённым ключом
session.execute("""
        CREATE TABLE IF NOT EXISTS bills_10000 (
            user_id TEXT,
            account_id TEXT,
            year INT,
            month INT,
            dt_uuid TIMEUUID,
            week_of_year INT,
            operation_id BIGINT,
            type TEXT,
            amount FLOAT,
            description TEXT,
            full_timestamp TIMESTAMP,
            data_create TIMESTAMP,
            PRIMARY KEY ((user_id, account_id, year, month), dt_uuid)
        )
    """)

# Закрытие соединения
cluster.shutdown()
