 
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


https://medium.com/ksquare-inc/how-to-use-apache-cassandras-stress-tool-a-step-by-step-guide-649ea26daa5d
docker exec -it cassandra1 /opt/cassandra/tools/bin/cassandra-stress  write n=100000 -schema "replication(strategy=NetworkTopologyStrategy,datacenter1=3)"