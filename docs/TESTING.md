 
RUN Cassandra cluster 
docker-compose up -d
docker exec -it cassandra1 nodetool status

Generate DATA
python scripts/generate_rows.py
python scripts/pg_reseipt/generate_rows.py
python scripts/pg_reseipt/generate_rows_copy.py

COPY pgs_receipt.bills_10000 (user_id, account_id, year, month, week_of_year, operation_id, type, amount, description, full_timestamp) FROM 'var/lib/cassandra/data_to_load.csv' WITH DELIMITER=',' AND HEADER=TRUE;

docker exec -it cassandra1 nodetool status
docker exec -it cassandra1 cqlsh -e "SELECT * FROM pgs_receipt.bills_10000 where user_id='user_25' and account_id='account_user_25' and year=2023 and month=7;"

Test perfomance
to-do


https://docs.datastax.com/en/dse/5.1/docs/tooling/cassandra-stress-tool.html
https://docs.datastax.com/en/archived/cassandra/3.0/cassandra/tools/toolsCStressOutput.html
docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress  write n=100000 -schema "replication(strategy=NetworkTopologyStrategy,datacenter1=3)"

# Insert (write) one million rows
$ docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress write n=1000000 -rate threads=5
# Read two hundred thousand rows.
$ docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress read n=200000 -rate threads=5

# Read rows for a duration of 3 minutes.
$ docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress read duration=3m -rate threads=5

# Read 200,000 rows without a warmup of 50,000 rows first.
$ docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress read n=200000 no-warmup -rate threads=5

docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress user profile=opt/cassandra/tools/cqlstress-example.yaml n=1000000 'ops(insert=3,simple1=1)' no-warmup cl=QUORUM

 docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress user profile=/var/lib/cassandra/mytest.yaml n=1000000 'ops(insert=3,user_bills_by_week=1)' no-warmup cl=QUORUM


docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress user profile=/var/lib/cassandra/myrest_s.yaml n=10000  ops\(user_bills_last_14_days=1,user_bills_last_month=1\) no-warmup  -rate threads=5

docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress user profile=/var/lib/cassandra/updated_yaml_file.yaml n=1000000 -rate threads=50




-schema "replication(strategy=NetworkTopologyStrategy,datacenter1=3)"