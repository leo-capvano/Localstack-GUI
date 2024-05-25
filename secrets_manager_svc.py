import os

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_SM_CUSTOM_ENDPOINT_URL = os.environ.get("AWS_SM_CUSTOM_ENDPOINT_URL", "http://localhost:4566")


def list_secrets():
    client = boto3.client('secretsmanager', endpoint_url=AWS_SM_CUSTOM_ENDPOINT_URL, region_name='us-east-1')
    return client.list_secrets()


def upsert_secret(secret_id: str, secret_value: str):
    client = boto3.client('secretsmanager', endpoint_url=AWS_SM_CUSTOM_ENDPOINT_URL, region_name='us-east-1')
    secret_ids = list(map(lambda s: s.get("Name"), client.list_secrets().get("SecretList")))
    if secret_id not in secret_ids:
        client.create_secret(
            Name=secret_id,
            SecretString=secret_value,
        )
        print(f"created secret with id {secret_id} and value {secret_value}")
    else:
        client.put_secret_value(
            SecretId=secret_id,
            SecretString=secret_value,
        )
        print(f"updated secret with id {secret_id} and value {secret_value}")


def get_secret_value(secret_id: str):
    client = boto3.client('secretsmanager', endpoint_url=AWS_SM_CUSTOM_ENDPOINT_URL, region_name='us-east-1')
    return client.get_secret_value(SecretId=secret_id)


def describe_secret(secret_id: str):
    client = boto3.client('secretsmanager', endpoint_url=AWS_SM_CUSTOM_ENDPOINT_URL, region_name='us-east-1')
    return client.describe_secret(SecretId=secret_id)


def delete_secret(secret_id: str):
    client = boto3.client('secretsmanager', endpoint_url=AWS_SM_CUSTOM_ENDPOINT_URL, region_name='us-east-1')
    return client.delete_secret(SecretId=secret_id, ForceDeleteWithoutRecovery=True)
