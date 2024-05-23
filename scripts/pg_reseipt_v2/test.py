from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import statistics
import time
import random

# Connect to Cassandra
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()
session.set_keyspace('pgs_receipt_v2')

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
        current_start_date = start_date
        while current_start_date < end_date:
            current_end_date = (current_start_date + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
            if current_end_date > end_date:
                current_end_date = end_date
            
            # print(f"Querying for user: {user}, account: account_{user}, year: {current_start_date.year}, month: {current_start_date.month}, start_date: {current_start_date}, end_date: {current_end_date}")
            
            start_time = time.time()
            session.execute(query, [user, f"account_{user}", current_start_date.year, current_start_date.month, current_start_date, current_end_date])
            durations.append(time.time() - start_time)
            
            current_start_date = (current_start_date + timedelta(days=32)).replace(day=1)

    return min(durations), statistics.mean(durations), max(durations), sum(durations)

# Measurements for each group
end_date = datetime(2023, 9, 11)
for group, users in [("обычные пользователи", sample_users), ("специальные пользователи", special_users)]:
    for period, days in [("14 дней", 14), ("1 месяц", 30), ("2 месяца", 60)]:
        start_date = end_date - timedelta(days=days)
        print(f"\nGroup: {group}, Period: {period}, Days: {days}, Start date: {start_date}, End date: {end_date}")
        min_time, avg_time, max_time, total_time = measure_time(users, start_date, end_date)
        print(f"{group}, {period}: мин - {min_time:.2f} сек, среднее - {avg_time:.2f} сек, макс - {max_time:.2f} сек, всего - {total_time:.2f} сек")

# Close the connection
cluster.shutdown()
