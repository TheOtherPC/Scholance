import json
from decimal import Decimal
from pprint import pprint
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import boto3


def create_user_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.create_table(
        TableName='Users',
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


def create_team_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:9000")
    table = dynamodb.create_table(
        TableName='Teams',
        KeySchema=[
            {
                'AttributeName': 'team_name',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'team_name',
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


def create_project_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:10000")
    table = dynamodb.create_table(
        TableName='Projects',
        KeySchema=[
            {
                'AttributeName': 'project_name',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'project_name',
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


def load_user_data(user_list, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Users')
    for user in user_list:
        username = user['username']

        print("Loading Users Data: ", username)
        table.put_item(Item=user)


def load_team_data(team_list, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:9000")
    table = dynamodb.Table('Teams')
    for team in team_list:
        team_name = team['team_name']

        print("Loading Teams Data: ", team_name)
        table.put_item(Item=team)


def put_user(user):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Users')
    response = table.put_item(
        Item={
            'username': user['username'],
            'info': {
                'email': user['info']['email'],
                'password': user['info']['password'],
                'first_name': user['info']['first_name'],
                'last_name': user['info']['last_name'],
            },
            'employee': {
                'level': user['employee']['level'],
                'school': user['employee']['school'],
                'teams': user['employee']['teams'],
                'interests': user['employee']['interests'],
                'skills': user['employee']['skills'],
                'projects': user['employee']['skills']
            },
            'customer': {
                'business': user['customer']['business'],
                'projects': user['customer']['projects'],
                'phone_number': user['customer']['phone_number'],
            }
        }
    )
    return response


def put_team(team):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:9000")
    table = dynamodb.Table("Teams")
    response = table.put_item(
        Item={
            'team_name': team.team_name,
            'info': {
                'team_lead': team.team_lead,
                'team_members': team.team_members,
                'project': team.project
            }

        }
    )
    return response


def put_project(project):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:10000")
    table = dynamodb.Table("Projects")
    response = table.put_item(
        Item={
            'project_name': project.project_name,
            'info': {
                'workers': project.workers,
                'project_start': project.project_start,
                'project_end': project.project_end,
                'customer': project.customer.business, #.username
                'description': project.description,
                'size': project.size,
                'preview': project.preview,
                'payment': project.payment,
                'active': project.active,
                'finished': project.finished,
                'project_url': project.project_url,
                'applications': project.applications
            }
        }
    )
    return response


def get_user(username, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Users')

    try:
        response = table.get_item(
            Key={'username': username})
    except ClientError as er:
        print(er.response['Error']['Message'])
    else:
        return response['Item']


def get_team(team_name, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:9000")
    table = dynamodb.Table('Teams')

    try:
        response = table.get_item(
            Key={'team_name': team_name})
    except ClientError as er:
        print(er.response['Error']['Message'])
    else:
        return response['Item']


def get_project(project_name, dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:10000")
    table = dynamodb.Table('Projects')

    try:
        response = table.get_item(
            Key={'project_name': project_name})
    except ClientError as er:
        print(er.response['Error']['Message'])
    else:
        return response['Item']


def update_user(username, attribute, attribute_value):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Users')

    response = table.update_item(
        Key={
            'username': username,
        },
        UpdateExpression="set " + attribute + "=:c",
        ExpressionAttributeValues={
            ":c": attribute_value
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def update_team(team_name, attribute, attribute_value):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:9000")
    table = dynamodb.Table('Teams')

    response = table.update_item(
        Key={
            'team_name': team_name,
        },
        UpdateExpression="set " + attribute + "=:c",
        ExpressionAttributeValues={
            ":c": attribute_value
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def update_project(project_name, attribute, attribute_value):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:10000")
    table = dynamodb.Table('Projects')

    response = table.update_item(
        Key={
            'project_name': project_name,
        },
        UpdateExpression="set " + attribute + "=:c",
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
    table = dynamodb.Table('Users')

    response = table.delete_item(
        Key={
            'username': username,
        },
    )
    return response


def delete_team(team_name, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:9000")
    table = dynamodb.Table('Teams')

    response = table.delete_item(
        Key={
            'team_name': team_name,
        },
    )
    return response


def delete_project(project_name):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:10000")
    table = dynamodb.Table('Projects')

    response = table.delete_item(
        Key={
            'project_name': project_name,
        },
    )
    return response


def query_users(username, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to query
    table = dynamodb.Table('Users')
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    return response['Items']


def query_teams(team_name, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:9000"
    )
    table = dynamodb.Table('Teams')
    response = table.query(
        KeyConditionExpression=Key('team_name').eq(team_name)
    )
    return response['Items']


def query_projects(project_name):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:10000"
    )
    table = dynamodb.Table('Projects')
    response = table.query(
        KeyCondtionExpression=Key('project_name').eq(project_name)
    )
    return response['Items']


def scan_users(attribute):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Users')
    response = table.scan(ProjectionExpression="" + attribute + ", username")
    return response['Items']


def scan_teams(attribute):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:9000"
    )
    table = dynamodb.Table('Teams')
    response = table.scan(ProjectionExpression="" + attribute + ", team_name")
    return response['Items']


def scan_projects(attribute):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:10000"
    )
    table = dynamodb.Table('Projects')
    print(attribute + ", project_name")
    response = table.scan(ProjectionExpression= "info, project_name")
    return response['Items']


def get_all_users():
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000"
    )
    table = dynamodb.Table('Users')
    response = table.scan(ProjectionExpression="username")
    return response['Items']


def get_all_teams():
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:9000"
    )
    table = dynamodb.Table('Teams')
    response = table.scan(ProjectionExpression="team_name")
    return response['Items']


def get_all_projects():
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:10000"
    )
    table = dynamodb.Table('Projects')
    response = table.scan(ProjectionExpression="project_name")
    return response['Items']

def get_projects_table():
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:10000"
    )
    return dynamodb.Table('Projects')
    dynamo.update_user("something", "customer.projects", '["hi"]')


if __name__ == '__main__':
    pprint(get_user("something"))
