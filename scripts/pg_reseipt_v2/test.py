from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import statistics
import time
import random

# Connect to Cassandra
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()
session.set_keyspace('pgs_receipt')

# Read special_users from the file
with open("2_per_users.txt", "r") as file:
    special_users = [line.strip() for line in file.readlines()]

# Exclude special_users and pick 200 random users from 50,000
all_users = [f"user_{i}" for i in range(50000) if f"user_{i}" not in special_users]
sample_users = random.sample(all_users, 200)

def measure_time(users, start_date, end_date):
    query = session.prepare("""
        SELECT * FROM bills_10000
        WHERE user_id = ? AND account_id = ? AND year = ? AND month = ? AND dt_uuid >= minTimeuuid(?) AND dt_uuid <= maxTimeuuid(?)
    """)
    
    durations = []
    for user in users:
        start_time = time.time()
        session.execute(query, [user, f"account_{user}", start_date.year, start_date.month, start_date, end_date])
        durations.append(time.time() - start_time)

    return min(durations), statistics.mean(durations), max(durations)

# Measurements for each group
end_date = datetime(2023, 9, 11)
for group, users in [("обычные пользователи", sample_users), ("специальные пользователи", special_users)]:
    for period, days in [("14 дней", 14), ("1 месяц", 30), ("2 месяца", 60)]:
        start_date = end_date - timedelta(days=days)
        min_time, avg_time, max_time = measure_time(users, start_date, end_date)
        print(f"{group}, {period}: мин - {min_time:.2f} сек, среднее - {avg_time:.2f} сек, макс - {max_time:.2f} сек")

# Close the connection
cluster.shutdown()
