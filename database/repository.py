"""
Repository for interacting with the PickEm DynamoDB table.
"""
import os
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from database.constants import *
from database.dynamo import get_table
from database.models import Category, Option


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

    def remove(self, category, name: str) -> bool:
        response = self._table.query(
            IndexName=CATEGORY,
            KeyConditionExpression=Key(CATEGORY_ID).eq(category),
            FilterExpression=Attr(USER_ID).eq(_user) & Attr(NAME).eq(name),
            ProjectionExpression="user_id, created_at"
        )
        if not (items := response.get(ITEMS, ())):
            return False

        for item in items:
            self._table.delete_item(
                Key={USER_ID: item[USER_ID], CREATED_AT: item[CREATED_AT]}
            )
        return True

    def edit(self, category, name: str, interest=None, effort=None) -> bool:
        response = self._table.query(
            IndexName=CATEGORY,
            KeyConditionExpression=Key(CATEGORY_ID).eq(category),
            FilterExpression=Attr(USER_ID).eq(_user) & Attr(NAME).eq(name),
        )

        item = response.get(ITEMS, [None])[0]
        if item is None:
            raise ItemNotFoundError

        option = Option.from_dict(item)
        interest = interest or option.interest
        effort = effort or option.effort
        self._table.update_item(
            Key={
                USER_ID: option.user_id, CREATED_AT: option.created_at,
            },
            UpdateExpression="SET interest = :i, effort = :e",
            ExpressionAttributeValues={":i": interest, ":e": effort},
        )
        return True

    def add_category(self, category, name, interest, effort: str) -> bool:
        item = {
            USER_ID: _user,
            CREATED_AT: f"{datetime.now(timezone.utc).isoformat()}#{uuid4()}",
            CATEGORY_ID: category,
            NAME: name,
            INTEREST: interest,
            EFFORT: effort,
        }

        try:
            self._table.put_item(Item=item)
        except ClientError as e:
            raise RepositoryError from e
        return True


repo = PickEmRepo()
