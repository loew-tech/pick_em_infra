"""
Repository for interacting with the PickEm DynamoDB table.
"""
import os
from collections import namedtuple
from typing import Any

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

from database.constants import *
from database.dynamo import get_table
from database.models import Category

SelectionOption = namedtuple('Option', ['name', 'start', 'weight', 'category'])


class RepositoryError(Exception):
    """Base exception for repository errors."""


class ItemNotFound(RepositoryError):
    """Raised when an item is not found."""


_user = os.environ["DYNAMODB_USER"]


class PickemRepo:

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

    def pick(self, categories: list[str], interest, effort: str) -> Any:
        if not categories or interest not in TIERS or effort not in TIERS:
            raise RepositoryError

        return NotImplemented

    def _get_options(self, categories: list[str], interest: str, effort: str) -> list[SelectionOption]:
        i = {*TIERS[TIERS.index(interest):]}
        e = {*TIERS[:TIERS.index(effort) + 1]}
        options = []
        for c in categories:
            category = self.get_category(c).choices
            for d in category:
                if d.effort not in e or d.interest not in i:
                    continue
                start = options[-1].start + options[-1].weight if options else 0
                # @TODO: is this how I want to handle interest < effort
                wght = max(1, WEIGHTS[d.interest] // WEIGHTS[d.effort])
                options.append(SelectionOption(name=d.name, start=start, weight=wght,
                                               category=c))
        return options
