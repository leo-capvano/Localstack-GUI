import os

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_S3_CUSTOM_ENDPOINT_URL = os.environ.get("AWS_S3_CUSTOM_ENDPOINT_URL", "http://localhost:4566")


def list_buckets():
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL)
    return client.list_buckets().get("Buckets")


def list_objects(bucket_name: str) -> list:
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL)
    list_objects_response = client.list_objects_v2(Bucket=bucket_name)
    if list_objects_response.get("IsTruncated"):
        print("WARN - response truncated")
    if list_objects_response.get("KeyCount") > 0:
        return list_objects_response.get("Contents")
    else:
        print(f"WARN - any result found for bucket {bucket_name}")
        return []


def write_object(bucket_name: str, object_key: str, object_data: bytes):
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL)
    return client.put_object(Bucket=bucket_name, Key=object_key, Body=object_data)


def delete_object(bucket_name: str, object_key: str):
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL)
    return client.delete_object(Bucket=bucket_name, Key=object_key)


def get_object(bucket_name: str, object_key: str):
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL)
    return client.get_object(Bucket=bucket_name, Key=object_key)


def download_object(bucket_name: str, object_key: str, output_file_path: str):
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL)
    client.download_file(Bucket=bucket_name, Key=object_key, Filename=output_file_path)


def create_bucket(bucket_name: str):
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL, region_name="us-east-1")
    return client.create_bucket(Bucket=bucket_name)


def delete_bucket(bucket_name: str):
    client = boto3.client("s3", endpoint_url=AWS_S3_CUSTOM_ENDPOINT_URL)
    return client.delete_bucket(Bucket=bucket_name)


if __name__ == '__main__':
    buckets = list_buckets()
    for bucket in buckets:
        print(f"bucket name: {bucket.get("Name")} - creation date {bucket.get("CreationDate")}\n")
        objects = list_objects(bucket.get("Name"))
        for obj in objects:
            print(f"object: {obj}")
        print("------------------------------------------------------------------------------------------------------")
