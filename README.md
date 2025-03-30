# cassandra

[![Build Status](https://app.travis-ci.com/boosterKRD/cassandra.svg?branch=test)](https://app.travis-ci.com/boosterKRD/cassandra)

🧪 **Sandbox for Apache Cassandra experiments**  
This is a test environment for exploring Apache Cassandra, running clusters, writing data, and using various Cassandra tools and features.

---

## 🚀 Quick Start

**Run the Cassandra cluster and prepare the environment:**

```bash
make init
pipenv install
pipenv shell

#Run data generation and testing scripts
python scripts/pg_reseipt_v2/create_shcema.py
python scripts/pg_reseipt_v2/generate_rows.py
python scripts/pg_reseipt_v2/test.py
```

## 🛠️ Makefile Commands
```bash
make init      # Start the cluster
make reinit    # Restart it
make stop      # Stop and remove containers
make status    # Show container status
make clean     # Stop and remove data volumes
```


## 🧰 Useful Commands
### 🧪 Cassandra / Docker

```bash
docker-compose stop cassandra2`  
docker run -it --network docker_test --rm cassandra cqlsh cassandra
docker exec -it cassandra1 nodetool status
docker exec -it cassandra1 nodetool ring boost_1988
docker exec -it cassandra1 nodetool netstats
  
docker exec -it cassandra2 nodetool flush
docker exec -it cassandra3 nodetool repair
docker exec -it cassandra1 nodetool compact boost_1 tb1
docker exec -it cassandra1 cqlsh
nodetool --host 172.28.0.2 info
docker exec -it cassandra1 nodetool getendpoints boost_2 tb1 1
```

### 📊 Data Distribution

```bash
docker exec -it cassandra2 nodetool cfstats boost_3.tb1`
docker exec -it cassandra1 nodetool tablestats pgs_receipt.bills_10000`
```

## 🧾 Full Query Logging

[Docs: Full Query Logging](https://cassandra.apache.org/doc/latest/cassandra/operating/fqllogging.html)

```bash
# Enable full query logging
docker exec -it cassandra2 nodetool enablefullquerylog --path /tmp/cassandrafullquerylog

# Connect to Cassandra
docker exec -it cassandra2 cqlsh

CREATE KEYSPACE querylogkeyspace1 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE querylogkeyspace1;
CREATE TABLE t (id int, k int, v text, PRIMARY KEY (id));
INSERT INTO t (id, k, v) VALUES (0, 0, 'val0');
INSERT INTO t (id, k, v) VALUES (0, 1, 'val1');

# Dump logs
docker exec -it cassandra2 /opt/cassandra/tools/bin/fqltool dump /tmp/cassandrafullquerylog

# Disable logging
docker exec -it cassandra2 nodetool disablefullquerylog

# Drop keyspace
docker exec -it cassandra2 cqlsh -e "DROP KEYSPACE querylogkeyspace1;"

# Replay logs
docker exec -it cassandra2 /opt/cassandra/tools/bin/fqltool replay --keyspace querylogkeyspace --results /cassandra/fql/logs/results/replay --store-queries /cassandra/fql/logs/queries/replay --target 172.28.0.3 /tmp/cassandrafullquerylog
```

## 🔒 Audit Logging
[Docs: Audit Logging](https://cassandra.apache.org/doc/latest/cassandra/operating/auditlogging.html)

```bash
docker exec -it cassandra2 nodetool enableauditlog
docker exec -it cassandra2 cqlsh  # make some queries
docker exec -it cassandra2 nodetool disableauditlog
docker exec -it cassandra2 auditlogviewer /cassandra/audit/logs/hourly
```

## 🛠️ sstable-tools
Install sstable-tools

```bash
apt-get update
apt-get install -y python3 python3-pip liblz4-tool libsnappy1v5
pip3 install sstable-tools
```
Usage:
```bash
/opt/cassandra/tools/bin/sstabledump nb-6-big-Data.db
```

## 📈 Monitoring
```bash
docker exec -it cassandra1 nodetool tpstats | grep -E "Hint|HINT" #just an example
```

CREATE KEYSPACE boost_3 WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
DROP KEYSPACE boost_3;
create table tb1 (Id int primary key, name text,  city text ); 
SELECT * FROM system_schema.keyspaces;
describe keyspace booster_2

-----

## 📋 Useful SQL Queries
```sql
SELECT * FROM system_schema.keyspaces;
SELECT * FROM system_schema.tables WHERE keyspace_name = 'bills';
SELECT * FROM system_schema.columns WHERE keyspace_name = 'boost_2' AND table_name = 'tb1';

SELECT * FROM bills
WHERE user_id = 'user_4500'
  AND account_id = 'account_user_4500'
  AND year = 2023
  AND month = 9;

-- Example with UUID
SELECT * FROM bills
WHERE user_id = 4e48c1e9-e18e-4a49-b7c6-66e3769b219e
  AND account_id = 'account_4e48c1e9-e18e-4a49-b7c6-66e3769b219e'
  AND year = 2022
  AND month = 10
  AND week_of_year > 43
ORDER BY week_of_year ASC;

--Schema & Keyspaces
CREATE KEYSPACE boost_3 WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
DROP KEYSPACE boost_3;

CREATE TABLE tb1 (
  id int PRIMARY KEY,
  name text,
  city text
);

SELECT * FROM system_schema.keyspaces;
DESCRIBE KEYSPACE booster_2;
```


## 📚 Documentation (MkDocs)

You can view this project as a static HTML site using [MkDocs](https://www.mkdocs.org/).

### Option 1: Run a local dev server

```bash
brew install mkdocs
mkdocs serve
#Open in browser: http://127.0.0.1:8000
```

Option 2: Generate HTML files
```bash
mkdocs build
site/index.html
```