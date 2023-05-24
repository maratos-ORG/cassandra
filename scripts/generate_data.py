from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
import time

# Connect to the Cassandra cluster
cluster = Cluster(['172.28.250.2'], port=9042)
session = cluster.connect()

# prepare your queries
create_keyspace_query = """
CREATE KEYSPACE IF NOT EXISTS boost_3 
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3}
"""

create_table_query = """
CREATE TABLE IF NOT EXISTS boost_3.mytable (
  id int PRIMARY KEY,
  name text
)
"""

# create keyspace with consistency level of LOCAL_QUORUM
statement = SimpleStatement(create_keyspace_query, consistency_level=ConsistencyLevel.LOCAL_QUORUM)
session.execute(statement)

# Use the keyspace
session.set_keyspace('boost_3')

# create table with consistency level of LOCAL_QUORUM
statement = SimpleStatement(create_table_query, consistency_level=ConsistencyLevel.LOCAL_QUORUM)
session.execute(statement)

time.sleep(2)
# Generate 200,000 rows of data
for i in range(1, 5000):
    name = 'Name {}'.format(i)
    city = ['New York', 'London', 'Paris', 'Sydney', 'Tokyo'][i % 5]
    session.execute("INSERT INTO tb1 (id, name, city) VALUES (%s, %s, %s)", (i, name, city))

# Close the connection
session.shutdown()
cluster.shutdown()

