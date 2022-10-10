import json
from decimal import Decimal
from pprint import pprint
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import boto3


# also create a new table for customers

def create_employee_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.create_table(
        TableName='Employees',
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
        }
    )
    return table


def load_data(user_list, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Employees')
    for user in user_list:
        username = user['username']

        print("Loading Users Data: ", username)
        table.put_item(Item=user)


def put_employee(user):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Employees')
    response = table.put_item(
        Item={
            'username': user.username,
            'info': {
                'email': user.email,
                'password': user.password,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'level': user.level,
                'school': user.school,
                'team': user.team
            }
        }
    )
    return response


def get_employee(username, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Employees')

    try:
        response = table.get_item(
            Key={'username': username})
    except ClientError as er:
        print(er.response['Error']['Message'])
    else:
        return response['Item']


def update_employee(username, attribute, attribute_value):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Employees')

    response = table.update_item(
        Key={
            'username': username,
        },
        UpdateExpression="set info." + attribute + "=:c",
        ExpressionAttributeValues={
            ":c": attribute_value
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def delete_user(username, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to delete from
    table = dynamodb.Table('Employees')

    response = table.delete_item(
        Key={
            'username': username,
        },
    )

def query_employees(username, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to query
    table = dynamodb.Table('Employees')
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    return response['Items']



if __name__ == '__main__':
    '''
      employees_table = create_employee_table()
      # Print table status
      print("Status:", employees_table.table_status)
      '''

    '''
        with open("data.json") as json_file:
            employees_list = json.load(json_file, parse_float=Decimal)
        load_data(employees_list)
        '''
