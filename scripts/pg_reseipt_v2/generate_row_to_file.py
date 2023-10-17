import csv
from datetime import datetime, timedelta
import random

# Constants
OUTPUT_FILE = "data_to_load.csv"

# Start the CSV writing
with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'account_id', 'year', 'month', 'dt_uuid', 'week_of_year', 'operation_id', 'type', 'amount', 'description', 'full_timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Generating data
    start_date = datetime(2023, 9, 11) - timedelta(days=90)
    unique_users = [f"user_{i}" for i in range(35002, 50000)]

    max_ops_for_users = {}
    min_ops_for_users = {}
    special_users = random.sample(unique_users, int(0.003 * len(unique_users)))

    # Print the names of the special users
    print("0.3% of users with a minimum value of 10 and a maximum of 100:")
    for user in special_users:
        print(user)

    for user in special_users:
        max_ops_for_users[user] = 100
        min_ops_for_users[user] = 10

    operation_id_counter = 0

    for index, user_id in enumerate(unique_users, 1):
        account_id = f"account_{user_id}"
        current_date = start_date
        while current_date <= datetime(2023, 9, 11):

            if user_id in special_users:
                no_operation_probability = 0.15
            else:
                no_operation_probability = 0.35

            if random.random() < no_operation_probability:
                operations_today = 0
            else:
                operations_today = random.randint(min_ops_for_users[user_id], max_ops_for_users[user_id])

            for _ in range(operations_today):
                operation_id_counter += 1
                type_value = "transaction"
                amount = round(random.uniform(1.0, 1000.0), 2)
                description = "Sample transaction"
                full_timestamp = current_date.strftime('%Y-%m-%d %H:%M:%S')
                dt_uuid = full_timestamp
                writer.writerow({
                    'user_id': user_id,
                    'account_id': account_id,
                    'year': current_date.year,
                    'month': current_date.month,
                    'dt_uuid': dt_uuid,  # Replacing the 'now()' in Cassandra
                    'week_of_year': int(current_date.strftime("%U")),
                    'operation_id': operation_id_counter,
                    'type': type_value,
                    'amount': amount,
                    'description': description,
                    'full_timestamp': full_timestamp
                })
            current_date += timedelta(days=1)

        if index % 500 == 0:
            print(f"Processed {index} users")

print(f"Data generation complete. File saved as {OUTPUT_FILE}")
print(f"Run the following command in cqlsh to import the data:")
print(f"COPY pgs_receipt.bills_10000 (user_id, account_id, year, month, dt_uuid, week_of_year, operation_id, type, amount, description, full_timestamp) FROM '{OUTPUT_FILE}' WITH DELIMITER=',' AND HEADER=TRUE;")
