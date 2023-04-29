from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['localhost'], port=9044)
session = cluster.connect('booster_point')

# Generate 200,000 rows of data
for i in range(400000, 500000):
    name = 'Name {}'.format(i)
    city = ['New York', 'London', 'Paris', 'Sydney', 'Tokyo'][i % 5]
    session.execute("INSERT INTO tb1 (id, name, city) VALUES (%s, %s, %s)", (i, name, city))

# Close the connection
session.shutdown()
cluster.shutdown()

