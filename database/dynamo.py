"""
DynamoDB table access.
"""
import os

import boto3
from mypy_boto3_dynamodb.service_resource import Table

_dynamodb = boto3.resource("dynamodb")

_table = _dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def get_table() -> Table:
    return _table
