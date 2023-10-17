from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import statistics
import time
import random

# Подключение к Cassandra
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()
session.set_keyspace('pgs_receipt_v1')

# Read special_users from the file
with open("2_per_users.txt", "r") as file:
    special_users = [line.strip() for line in file.readlines()]
    
# Выберем 100 случайных пользователей, исключая специальных
all_users = [f"user_{i}" for i in range(50000) if f"user_{i}" not in special_users]
sample_users = random.sample(all_users, 200)

def measure_time(users, start_date, end_date):
    query = session.prepare("""
        SELECT * FROM bills_10000
        WHERE user_id = ? AND account_id = ? AND year = ? AND month = ? AND week_of_year >= ? AND week_of_year <= ?
    """)
    
    durations = []
    for user in users:
        start_time = time.time()
        current_year = start_date.year
        start_month = start_date.month
        start_week = int(start_date.strftime("%U"))
        end_week = int(end_date.strftime("%U"))
        session.execute(query, [user, f"account_{user}", current_year, start_month, start_week, end_week])
        durations.append(time.time() - start_time)

    min_time = min(durations)
    avg_time = sum(durations) / len(durations)
    max_time = max(durations)
    return min_time, avg_time, max_time


# Замеры для каждой группы
end_date = datetime(2023, 9, 11)
for group, users in [("обычные пользователи", sample_users), ("специальные пользователи", special_users)]:
    for period, days in [("14 дней", 14), ("1 месяц", 30), ("2 месяца", 60)]:
        start_date = end_date - timedelta(days=days)
        min_time, avg_time, max_time = measure_time(users, start_date, end_date)
        print(f"{group}, {period}: мин - {min_time:.2f} сек, среднее - {avg_time:.2f} сек, макс - {max_time:.2f} сек")

# Закрытие соединения
cluster.shutdown()
