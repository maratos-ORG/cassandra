from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from cassandra.query import BatchStatement
from concurrent.futures import ThreadPoolExecutor
import time

# Connect to the Cassandra cluster
cluster = Cluster(['172.28.250.2'], port=9042)
# cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()

# prepare your queries
create_keyspace_query = """
CREATE KEYSPACE IF NOT EXISTS boost_2 
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 2}
"""

create_table_query = """
CREATE TABLE IF NOT EXISTS boost_2.tb1 (
  id int PRIMARY KEY,
  name text,
  city text
)
"""

# create keyspace with consistency level of LOCAL_QUORUM
statement = SimpleStatement(create_keyspace_query, consistency_level=ConsistencyLevel.ALL)
session.execute(statement)
time.sleep(2)
# Use the keyspace
session.set_keyspace('boost_2')

# create table with consistency level of LOCAL_QUORUM
statement = SimpleStatement(create_table_query, consistency_level=ConsistencyLevel.ALL)
session.execute(statement)
time.sleep(2)
# # #----------BATCH INSERT
batch = BatchStatement(consistency_level=ConsistencyLevel.LOCAL_ONE)
for i in range(1, 10000):
    name = 'Name {}'.format(i)
    city = ['New York', 'London', 'Paris', 'Sydney', 'Tokyo'][i % 5]
    batch.add("INSERT INTO tb1 (id, name, city) VALUES (%s, %s, %s)", (i, name, city))
    if len(batch) >= 500:  # choose a suitable batch size; maybe 50 or 100
        session.execute(batch)
        batch.clear()
if len(batch) > 0:
    session.execute(batch)
    
# #-------------PREPARE INSERT-----
# insert_query = session.prepare("INSERT INTO tb1 (id, name, city) VALUES (?, ?, ?)")
# for i in range(1, 10000):
#     name = 'Name {}'.format(i)
#     city = ['New York', 'London', 'Paris', 'Sydney', 'Tokyo'][i % 5]
#     bound_statement = insert_query.bind((i, name, city))
#     bound_statement.consistency_level = ConsistencyLevel.LOCAL_QUORUM
#     session.execute(bound_statement)


#--------------STANDART INSERT-------
# # # create table with consistency level of LOCAL_QUORUM
# # statement = SimpleStatement(create_table_query, consistency_level=ConsistencyLevel.ALL)
# # session.execute(statement)

# # # Generate 10,000 rows of data
# # for i in range(1, 10000):
# #     name = 'Name {}'.format(i)
# #     city = ['New York', 'London', 'Paris', 'Sydney', 'Tokyo'][i % 5]
# #     session.execute("INSERT INTO tb1 (id, name, city) VALUES (%s, %s, %s)", (i, name, city)) 

# Close the connection
session.shutdown()
cluster.shutdown()

