import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal
import uuid
import random
from datetime import datetime, timedelta
import time

# Подключение к DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')

# Функция для создания таблицы
def create_table(table_name):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'user_account',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'year_month_day_timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_account',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'year_month_day_timestamp',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # Используем режим on-demand
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} created successfully.")
        return table
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

# Функция для получения таблицы
def get_table(table_name):
    try:
        table = dynamodb.Table(table_name)
        table.load()
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return None
        else:
            raise

# Функция для создания индекса
def create_index(table, index_name, key_schema):
    try:
        table.update(
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_account',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': key_schema['RANGE']['AttributeName'],
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': index_name,
                        'KeySchema': [
                            {
                                'AttributeName': 'user_account',
                                'KeyType': 'HASH'  # Partition key
                            },
                            {
                                'AttributeName': key_schema['RANGE']['AttributeName'],
                                'KeyType': 'RANGE'  # Sort key
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        }
                    }
                }
            ]
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table.name)
        print(f"GSI {index_name} created successfully.")
    except ClientError as e:
        print(e.response['Error']['Message'])

# Функция для ожидания активации индекса
def wait_for_index_active(table_name, index_name):
    client = boto3.client('dynamodb', region_name='eu-north-1')
    while True:
        response = client.describe_table(TableName=table_name)
        indexes = response['Table'].get('GlobalSecondaryIndexes', [])
        for index in indexes:
            if index['IndexName'] == index_name and index['IndexStatus'] == 'ACTIVE':
                print(f"GSI {index_name} is active.")
                return
        time.sleep(10)

# Функция для генерации случайной даты в указанном диапазоне
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

# Основное тело скрипта
table_name = 'bills'
table = get_table(table_name)

if table is None:
    table = create_table(table_name)

# Проверка и создание индексов
if table is not None:
    index_name = 'UserAccountTypeIndex'
    create_index(table, index_name, {'RANGE': {'AttributeName': 'type'}})
    wait_for_index_active(table_name, index_name)

    index_name = 'UserAccountTypeTimestampIndex'
    create_index(table, index_name, {'RANGE': {'AttributeName': 'type_timestamp'}})
    wait_for_index_active(table_name, index_name)

    # Генерация и вставка данных
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    for _ in range(100):
        unique_id = str(uuid.uuid4())  # Генерация уникального идентификатора
        date = random_date(start_date, end_date)
        year_month_day = date.strftime('%Y#%m#%d')

        item = {
            'user_account': f'user{random.randint(1, 5)}#account{random.randint(1, 5)}',
            'year_month_day_timestamp': f'{year_month_day}#{unique_id}',
            'week_of_year': date.isocalendar()[1],
            'operation_id': random.randint(1000000000, 9999999999),
            'type': random.choice(['income', 'expense']),
            'amount': Decimal(str(random.uniform(10.0, 1000.0))),
            'description': random.choice(['Monthly bill payment', 'Purchase', 'Salary', 'Refund']),
            'full_timestamp': date.isoformat(),
            'data_create': date.isoformat(),
            'type_timestamp': f'{random.choice(["income", "expense"])}#{year_month_day}'  # Составной ключ для сортировки
        }

        try:
            table.put_item(Item=item)
            print(f"Item inserted successfully: {item}")
        except ClientError as e:
            print(e.response['Error']['Message'])
