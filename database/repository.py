# import os
# from typing import Any
#
# import boto3
# from boto3.dynamodb.conditions import Key
# from cachetools import TTLCache, cached
#
# # from boto3.resources.base import ServiceResource
#
# # from mypy_boto3_dynamodb.service_resource import Table
#
# from database.constants import *
#
# cache = TTLCache(maxsize=100, ttl=60)
#
# _dynamodb = boto3.resource("dynamodb")
# # @TODO: add this to stack
# # table = dynamodb.Table(
# #     self,
# #     "PickEmTable",
# #     partition_key=...,
# # )
# #
# # my_lambda = _lambda.Function(
# #     self,
# #     "CreatePick",
# #     ...
# #     environment={
# #         "TABLE_NAME": table.table_name,
# #     },
# # )
# _table = _dynamodb.Table(os.environ["DYNAMODB_TABLE"])
# # @TODO: remove hard code and introduce some kind user management
# _user = os.environ["DYNAMODB_USER"]
#
#
# def categories() -> list[Any]:
#     response = _table.query(
#         KeyConditionExpression=Key(USER_ID).eq(_user),
#         ProjectionExpression=CATEGORY_ID
#     )
#     return sorted({item[CATEGORY_ID] for item in response.get(ITEMS, [])})
#
#
# @cached(cache)
# def category(category: str) -> Any:
#     response = _table.query(
#         IndexName=CATEGORY,
#         KeyConditionExpression=Key(CATEGORY).eq(category),
#         FIlterExpression=Attr(USER_ID).eq(_user),
#         ProjectionExpression="#n, effort, interest",
#         ExpressionAttributeNames={"#n": NAME}
#     )
#     return {NAME: category, CHOICES: response.get(ITEMS, [])}
#
#
# def pick(categories, interest, effort: str) -> Any:
#     if not cats or i not in TIERS or e not in TIERS: