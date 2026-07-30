"""
Repository for interacting with the PickEm DynamoDB table.
"""
import os
from collections import namedtuple
from random import randint
from typing import Any

from boto3.dynamodb.conditions import Key, Attr
# from botocore.exceptions import ClientError

from database.constants import *
from database.dynamo import get_table
from database.models import Category
from services.pick import pick


class RepositoryError(Exception):
    """Base exception for repository errors."""


class ItemNotFoundError(RepositoryError):
    """Raised when an item is not found."""


_user = os.environ["DYNAMODB_USER"]


class PickEmRepo:

    def __init__(self):
        self._table = get_table()

    def categories(self) -> list[Any]:
        response = self._table.query(
            KeyConditionExpression=Key(CATEGORY).eq(_user),
            ProjectionExpression=CATEGORY_ID,
        )
        return sorted(item[CATEGORY_ID] for item in response.get(ITEMS, []))

    def get_category(self, category: str) -> Category:
        response = self._table.query(
            IndexName=CATEGORY,
            KeyConditionExpression=Key(CATEGORY_ID).eq(category),
            FilterExpression=Attr(USER_ID).eq(_user),
            ProjectionExpression="#n, effort, interest",
            ExpressionAttributeNames={"#n": NAME}
        )
        return Category.from_dict({NAME: category, CHOICES: response.get(ITEMS, [])})


repo = PickEmRepo()
