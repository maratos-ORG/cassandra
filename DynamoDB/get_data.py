import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# Подключение к DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')

# Функция для получения таблицы
def get_table(table_name):
    try:
        table = dynamodb.Table(table_name)
        table.load()
        return table
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

# Функция для выполнения запроса по диапазону дат
def query_date_range(table, user_id, account_id, start_date, end_date):
    try:
        response = table.query(
            KeyConditionExpression=Key('user_account').eq(f'{user_id}#{account_id}') &
                                 Key('year_month_day_timestamp').between(start_date, end_date)
        )
        return response['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
        return []

# Функция для выполнения запроса по индексу 1
def query_by_type(table, user_account, query_type, index_name):
    try:
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key('user_account').eq(user_account) & Key('type').eq(query_type)
        )
        return response['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
        return []

# Функция для выполнения запроса по индексу 2 с диапазоном дат
def query_by_type_and_date_range(table, user_account, query_type, start_date, end_date, index_name):
    try:
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key('user_account').eq(user_account) & Key('type_timestamp').between(f'{query_type}#{start_date}', f'{query_type}#{end_date}')
        )
        return response['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
        return []

# Основное тело скрипта
table_name = 'bills'
table = get_table(table_name)

if table is not None:
    # Выполнение запросов
    user_id = 'user2'
    account_id = 'account3'

    # Запрос 1: Диапазон дат
    start_date = '2023#04#07'
    end_date = '2023#05#07'
    result = query_date_range(table, user_id, account_id, start_date, end_date)
    print("Query 1 result:")
    for item in result:
        print(item)

    # Запрос 2: Индекс 1
    user_account = 'user2#account3'
    query_type = 'income'
    index_name = 'UserAccountTypeIndex'
    result = query_by_type(table, user_account, query_type, index_name)
    print("Query 2 result:")
    for item in result:
        print(item)

    # Запрос 3: Индекс 2 с диапазоном дат
    user_account = 'user2#account3'
    query_type = 'income'
    start_date = '2023#03#01'
    end_date = '2023#08#30'
    index_name = 'UserAccountTypeTimestampIndex'
    result = query_by_type_and_date_range(table, user_account, query_type, start_date, end_date, index_name)
    print("Query 3 result:")
    for item in result:
        print(item)
else:
    print("Table does not exist.")
