# 🧪 DynamoDB Sandbox

This folder contains a test environment for **AWS DynamoDB**, designed to **mirror the logic and schema used in the Cassandra sandbox**.  
The goal is to **compare behavior** between Cassandra and DynamoDB using the same data model and operations.

---

## 🚀 Quick Start

```bash
cd maratos-ORG
pipenv install
pipenv shell
```

### 📦 Create Table, Indexes & Generate Data
```bash 
python3 DynamoDB/all_in_one.py
```

### 🔍 Query / Get Data
```bash
python3 DynamoDB/get_data.py
```

P.S. Schema, data generation, and access patterns are intentionally aligned with the Cassandra test setup.