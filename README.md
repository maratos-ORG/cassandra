###TRAVIC CI STATUS. 

Travic CI status: [![Build Status](https://app.travis-ci.com/boosterKRD/cassandra.svg?branch=test)](https://app.travis-ci.com/boosterKRD/cassandra)

### Main
**run cassandra cluster**  
`docker-compose up -d`
<!-- `python scripts/generate_data.py` -->
`python scripts/pg_reseipt/create_shcema.py`
`python scripts/pg_reseipt_v2/create_shcema.py`
`python scripts/pg_reseipt/generate_rows.py`
`python scripts/pg_reseipt_v2/generate_rows.py`
`python scripts/pg_reseipt/test.py`
`python scripts/pg_reseipt_v2/test.py`

select user_id,  year, month, toDate(dt_uuid), dt_uuid, data_create from bills_10000 where user_id='user_55' and account_id='account_user_55' and year=2023 and month=9 and dt_uuid >  maxTimeuuid('2023-09-01 00:00:00+0000') and dt_uuid <  maxTimeuuid('2023-09-04 00:00:00+0000');
### Usful cmd

`docker-compose stop cassandra2`  
`docker run -it --network docker_test --rm cassandra cqlsh cassandra` 
`docker exec -it cassandra1 nodetool status`  
`docker exec -it cassandra1 nodetool ring boost_1988`
`docker exec -it cassandra1 nodetool netstats`
  
`docker exec -it cassandra2 nodetool flush`
`docker exec -it cassandra3 nodetool repair`
`docker exec -it cassandra1 nodetool compact boost_1 tb1`
`docker exec -it cassandra1 cqlsh`  
`nodetool --host 172.28.0.2 info`
`docker exec -it cassandra1 nodetool getendpoints boost_2 tb1 1` 

 select * from dse_perf.user_io;

 DATA Distribution
 `docker exec -it cassandra2 nodetool cfstats boost_3.tb1`
 `docker exec -it cassandra1 nodetool tablestats pgs_receipt.bills_10000`
 
LOGS -> https://cassandra.apache.org/doc/latest/cassandra/operating/fqllogging.html
1. docker exec -it cassandra2 nodetool enablefullquerylog --path /tmp/cassandrafullquerylog
2. docker exec -it cassandra2 cqlsh    
    CREATE KEYSPACE querylogkeyspace1 WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
    USE querylogkeyspace1;
    CREATE TABLE t (id int,k int,v text,PRIMARY KEY (id));
    INSERT INTO t (id, k, v) VALUES (0, 0, 'val0');
    INSERT INTO t (id, k, v) VALUES (0, 1, 'val1');
3. docker exec -it cassandra2 /opt/cassandra/tools/bin/fqltool dump /tmp/cassandrafullquerylog  
4. docker exec -it cassandra2 nodetool disablefullquerylog
5. docker exec -it cassandra2 cqlsh 
     DROP KEYSPACE querylogkeyspace1;
6. docker exec -it cassandra2 /opt/cassandra/tools/bin/fqltool replay --keyspace querylogkeyspace --results /cassandra/fql/logs/results/replay --store-queries /cassandra/fql/logs/queries/replay --target 172.28.0.3 /tmp/cassandrafullquerylog

Audit Logging -> https://cassandra.apache.org/doc/latest/cassandra/operating/auditlogging.html
docker exec -it cassandra2 nodetool enableauditlog 
docker exec -it cassandra2 cqlsh -- make some queries
docker exec -it cassandra2 nodetool disableauditlog
docker exec -it cassandra2 auditlogviewer /cassandra/audit/logs/hourly





CREATE KEYSPACE boost_3 WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
DROP KEYSPACE boost_3;
create table tb1 (Id int primary key, name text,  city text ); 
SELECT * FROM system_schema.keyspaces;
describe keyspace booster_2



-----Install sstable-tools
apt-get update
apt-get install -y python3 python3-pip liblz4-tool libsnappy1v5
pip3 install sstable-tools
 /opt/cassandra/tools/bin/sstabledump nb-6-big-Data.db


Monitoring
docker exec -it cassandra1 nodetool tpstats | grep -E "Hint|HINT"
 

SQL usful
SELECT * FROM system_schema.keyspaces;
SELECT * FROM system_schema.tables WHERE keyspace_name = 'bills';
SELECT * FROM system_schema.columns WHERE keyspace_name = 'boost_2' AND table_name = 'tb1';

nodetool tablestats boost_2.tb1



SELECT * FROM bills where user_id='user_4500' and account_id='account_user_4500' and year=2023 and 
month=9;

# SELECT * FROM bills  WHERE user_id=4e48c1e9-e18e-4a49-b7c6-66e3769b219e  AND account_id='account_4e48c1e9-e18e-4a49-b7c6-66e3769b219e'  AND year=2022 AND month=10 and week_of_year>43  ORDER BY week_of_year ASC;