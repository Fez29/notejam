from notejam import app
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json

"""AWS Secrets Manager"""

import boto3
import base64
from botocore.exceptions import ClientError

"""def get_secret():"""

secret_name_value = os.environ['mySql_secret_name']
region_name_value = os.environ['mySql_region_name']

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name_value
)

# In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
# See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
# We rethrow the exception by default.

try:
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name_value
    )
except ClientError as e:
    if e.response['Error']['Code'] == 'DecryptionFailureException':
        # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'InternalServiceErrorException':
        # An error occurred on the server side.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'InvalidParameterException':
        # You provided an invalid value for a parameter.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'InvalidRequestException':
        # You provided a parameter value that is not valid for the current state of the resource.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'ResourceNotFoundException':
        # We can't find the resource that you asked for.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
else:
    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

database_secrets = json.loads(get_secret_value_response['SecretString'])

app.config['SQLALCHEMY_DATABASE_URI'] =\
        ('mysql://{ENV_username}:{ENV_password}@{ENV_server}:{ENV_port}/{ENV_database}}'.format(
            ENV_username = os.environ['mySql_Username'],
            ENV_password = database_secrets['password'],
            ENV_server = os.environ['mySql_Server'],
            ENV_port = os.environ['mySql_Port'],
            ENV_database = os.environ['mySql_Database']
        ))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
