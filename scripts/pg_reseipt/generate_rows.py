from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import random
from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement

# Подключение к Cassandra
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()
session.set_keyspace('pgs_receipt')

# Подготовка запроса
insert_query = session.prepare("""
    INSERT INTO bills_10000 (user_id, account_id, year, month, week_of_year, operation_id, type, amount, description, full_timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""")

# Генерация данных
start_date = datetime(2023, 9, 11) - timedelta(days=90)  # начало 3 месяца назад
# unique_users = [f"user_{i}" for i in range(10000)]
unique_users = [f"user_{i}" for i in range(14501, 20001)]

# Установка максимального и минимального количества операций для каждого пользователя
max_ops_for_users = {}
min_ops_for_users = {}

# Выбираем 2% пользователей
special_users = random.sample(unique_users, int(0.02 * len(unique_users)))

# Выводим имена этих 2% пользователей
print("2% пользователей с минимальным значением 10 и максимальным 100:")
for user in special_users:
    print(user)
    max_ops_for_users[user] = 100
    min_ops_for_users[user] = 10

# Устанавливаем значения для остальных пользователей
for user_id in unique_users:
    if user_id not in max_ops_for_users:
        max_ops_for_users[user_id] = 15
        min_ops_for_users[user_id] = 1

operation_id_counter = 0

for index, user_id in enumerate(unique_users, 1):
    account_id = f"account_{user_id}"
    current_date = start_date
    while current_date <= datetime(2023, 9, 11):
        batch = BatchStatement(consistency_level=ConsistencyLevel.ONE)

        if user_id in special_users:
            no_operation_probability = 0.15
        else:
            no_operation_probability = 0.35

        if random.random() < no_operation_probability:  # probability for no operations
            operations_today = 0
        else:
            operations_today = random.randint(min_ops_for_users[user_id], max_ops_for_users[user_id])

        for _ in range(operations_today):
            operation_id_counter += 1
            type_value = "transaction"
            amount = round(random.uniform(1.0, 1000.0), 2)
            description = "Sample transaction"
            full_timestamp = current_date
            batch.add(insert_query, [user_id, account_id, current_date.year, current_date.month, int(current_date.strftime("%U")), operation_id_counter, type_value, amount, description, full_timestamp])
        
        # execute the batch
        if len(batch):  # Check if there's anything to execute
            session.execute(batch)
        current_date += timedelta(days=1)

    # Вывод прогресса каждые 500 пользователей
    if index % 500 == 0:
        print(f"Обработано {index} пользователей")

# Закрытие соединения
cluster.shutdown()
