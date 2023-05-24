from cassandra.cluster import Cluster
import time

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()

# Create a keyspace
session.execute("""
CREATE KEYSPACE IF NOT EXISTS boost_3 
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
""")
time.sleep(2)
# Use the keyspace
session.set_keyspace('boost_3')

# Create a table 
session.execute("""
CREATE TABLE IF NOT EXISTS tb1 (
Id int PRIMARY KEY,
name text,
city text);
""")
time.sleep(2)
# Generate 200,000 rows of data
for i in range(1, 1000):
    name = 'Name {}'.format(i)
    city = ['New York', 'London', 'Paris', 'Sydney', 'Tokyo'][i % 5]
    session.execute("INSERT INTO tb1 (id, name, city) VALUES (%s, %s, %s)", (i, name, city))

# Close the connection
session.shutdown()
cluster.shutdown()

