from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb,
    # aws_sqs as sqs,
)
from constructs import Construct


class PickEmStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self, "PickEmTable",
            table_name="PickEmTable",
            partition_key=dynamodb.Attribute(
                name='user_id',
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name='created_at',
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        table.add_global_secondary_index(
            index_name="category",
            partition_key=dynamodb.Attribute(
                name='category_id',
                type=dynamodb.AttributeType.STRING
            )
        )
