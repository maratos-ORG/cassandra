### Main
**run cassandra cluster**  
`docker-compose up -d`


### Usful cmd

`docker-compose stop cassandra2`  
`docker run -it --network docker_test --rm cassandra cqlsh cassandra` 


`docker exec -it cassandra-cassandra-1 nodetool status`  

`docker exec -it cassandra-cassandra3-1 nodetool flush`
`docker exec -it cassandra-cassandra3-1 nodetool compact booster_new tb1`
`docker exec -it cassandra-cassandra-1 cqlsh`  
`nodetool --host 172.28.0.2 info`
`docker exec -it cassandra-cassandra-1 nodetool getendpoints booster_new tb1 1` 



CREATE KEYSPACE booster_new2 WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};
DROP KEYSPACE booster_3;

create table tb3 (Id int primary key, name text,  city text ); 

SELECT * FROM system_schema.keyspaces;
describe keyspace booster_2



-----Install sstable-tools
apt-get update
apt-get install -y python3 python3-pip liblz4-tool libsnappy1v5
pip3 install sstable-tools
 /opt/cassandra/tools/bin/sstabledump nb-6-big-Data.db