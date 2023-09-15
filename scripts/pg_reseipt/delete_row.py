from cassandra.cluster import Cluster

# Connect to Cassandra
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect('pgs_receipt')

# Define 
year = 2023
month = 9

# Iterate over each user_id individually
for user_id in ["user" + str(i) for i in range(14501, 16000)]:
    # Fetch rows for the current user_id
    select_query = """
    SELECT user_id, account_id, year, month, week_of_year, operation_id 
    FROM bills_10000 
    WHERE user_id = %s AND account_id = %s AND year = %s AND month = %s
    """
    rows = session.execute(select_query, (user_id, 'account_' + user_id, year, month))

    # Loop through each record for the user_id and delete them
    for row in rows:
        delete_query = """
            DELETE FROM bills_10000 
            WHERE user_id = %s AND account_id = %s AND year = %s AND month = %s AND week_of_year = %s AND operation_id = %s
        """
        session.execute(delete_query, (row.user_id, row.account_id, row.year, row.month, row.week_of_year, row.operation_id))

# Close the connection
cluster.shutdown()
