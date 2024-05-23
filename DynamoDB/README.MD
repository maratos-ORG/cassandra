```bash
cd maratos-ORG
pipenv install
pipenv shell
```

Create Table/indexis/generate-data
    python3 DynamoDB/all_in_one.py
Get data    
    python3 DynamoDB/get_data.py




The similar table structure for Cassandra is as follows    

CREATE TABLE bills (
    user_account text,
    year_month_day timestamp,
    unique_id text,
    week_of_year int,
    operation_id bigint,
    type text,
    amount decimal,
    description text,
    full_timestamp timestamp,
    data_create timestamp,
    PRIMARY KEY ((user_account), year_month_day, unique_id)
);

CREATE TABLE bills_by_type (
    user_account text,
    type text,
    unique_id text,
    year_month_day timestamp,
    week_of_year int,
    operation_id bigint,
    amount decimal,
    description text,
    full_timestamp timestamp,
    data_create timestamp,
    PRIMARY KEY ((user_account), type, unique_id)
);

CREATE TABLE bills_by_type_and_date (
    user_account text,
    type text,
    year_month_day timestamp,
    unique_id text,
    week_of_year int,
    operation_id bigint,
    amount decimal,
    description text,
    full_timestamp timestamp,
    data_create timestamp,
    PRIMARY KEY ((user_account), type, year_month_day, unique_id)
);


-- Вставка данных
INSERT INTO bills (user_account, year_month_day, unique_id, week_of_year, operation_id, type, amount, description, full_timestamp, data_create)
VALUES 
('user1#account1', '2023-05-01T00:00:00Z', 'uniqueid1', 18, 1234567890, 'income', 600.0, 'Monthly bill payment', '2023-05-01T12:34:56Z', '2023-05-01T12:34:56Z'),
('user2#account2', '2023-05-15T00:00:00Z', 'uniqueid2', 20, 2234567890, 'expense', 250.0, 'Purchase', '2023-05-15T14:22:33Z', '2023-05-15T14:22:33Z'),
('user3#account3', '2023-06-10T00:00:00Z', 'uniqueid3', 24, 3234567890, 'income', 800.0, 'Salary', '2023-06-10T08:45:12Z', '2023-06-10T08:45:12Z'),
('user4#account4', '2023-07-01T00:00:00Z', 'uniqueid4', 27, 4234567890, 'expense', 100.0, 'Refund', '2023-07-01T19:00:00Z', '2023-07-01T19:00:00Z');

-- Вставка данных
INSERT INTO bills_by_type (user_account, type, unique_id, year_month_day, week_of_year, operation_id, amount, description, full_timestamp, data_create)
VALUES 
('user1#account1', 'income', 'uniqueid1', '2023-05-01T00:00:00Z', 18, 1234567890, 600.0, 'Monthly bill payment', '2023-05-01T12:34:56Z', '2023-05-01T12:34:56Z'),
('user2#account2', 'expense', 'uniqueid2', '2023-05-15T00:00:00Z', 20, 2234567890, 250.0, 'Purchase', '2023-05-15T14:22:33Z', '2023-05-15T14:22:33Z'),
('user3#account3', 'income', 'uniqueid3', '2023-06-10T00:00:00Z', 24, 3234567890, 800.0, 'Salary', '2023-06-10T08:45:12Z', '2023-06-10T08:45:12Z'),
('user4#account4', 'expense', 'uniqueid4', '2023-07-01T00:00:00Z', 27, 4234567890, 100.0, 'Refund', '2023-07-01T19:00:00Z', '2023-07-01T19:00:00Z');

-- Вставка данных
INSERT INTO bills_by_type_and_date (user_account, type, year_month_day, unique_id, week_of_year, operation_id, amount, description, full_timestamp, data_create)
VALUES 
('user1#account1', 'income', '2023-05-01T00:00:00Z', 'uniqueid1', 18, 1234567890, 600.0, 'Monthly bill payment', '2023-05-01T12:34:56Z', '2023-05-01T12:34:56Z'),
('user2#account2', 'expense', '2023-05-15T00:00:00Z', 'uniqueid2', 20, 2234567890, 250.0, 'Purchase', '2023-05-15T14:22:33Z', '2023-05-15T14:22:33Z'),
('user3#account3', 'income', '2023-06-10T00:00:00Z', 'uniqueid3', 24, 3234567890, 800.0, 'Salary', '2023-06-10T08:45:12Z', '2023-06-10T08:45:12Z'),
('user4#account4', 'expense', '2023-07-01T00:00:00Z', 'uniqueid4', 27, 4234567890, 100.0, 'Refund', '2023-07-01T19:00:00Z', '2023-07-01T19:00:00Z');


SELECT * FROM bills
WHERE user_account = 'user123#account456'
AND year_month_day >= '2023-05-01T00:00:00Z'
AND year_month_day <= '2023-05-31T23:59:59Z';

SELECT * FROM bills_by_type
WHERE user_account = 'user123#account456'
AND type = 'income';

SELECT * FROM bills_by_type_and_date
WHERE user_account = 'user123#account456'
AND type = 'income'
AND year_month_day >= '2023-06-01T00:00:00Z'
AND year_month_day <= '2023-06-30T23:59:59Z';




Here is another version with TIMEUUID
 CREATE TABLE bills (
    user_account text,
    time_uuid timeuuid,
    week_of_year int,
    operation_id bigint,
    type text,
    amount decimal,
    description text,
    full_timestamp timestamp,
    data_create timestamp,
    PRIMARY KEY ((user_account), time_uuid)
);

-- Вставка данных
INSERT INTO bills (user_account, time_uuid, week_of_year, operation_id, type, amount, description, full_timestamp, data_create)
VALUES 
('user1#account1', now(), 18, 1234567890, 'income', 600.0, 'Monthly bill payment', '2023-05-01T12:34:56Z', '2023-05-01T12:34:56Z'),
('user2#account2', now(), 20, 2234567890, 'expense', 250.0, 'Purchase', '2023-05-15T14:22:33Z', '2023-05-15T14:22:33Z'),
('user3#account3', now(), 24, 3234567890, 'income', 800.0, 'Salary', '2023-06-10T08:45:12Z', '2023-06-10T08:45:12Z'),
('user4#account4', now(), 27, 4234567890, 'expense', 100.0, 'Refund', '2023-07-01T19:00:00Z', '2023-07-01T19:00:00Z');

SELECT * FROM bills
WHERE user_account = 'user123#account456'
AND time_uuid >= minTimeuuid('2023-05-01T00:00:00Z')
AND time_uuid <= maxTimeuuid('2023-05-31T23:59:59Z');
