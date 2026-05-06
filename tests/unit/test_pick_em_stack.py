import aws_cdk as core
import aws_cdk.assertions as assertions

from pick_em.pick_em_stack import PickEmStack

# example tests. To run these tests, uncomment this file along with the example
# resource in pick_em/pick_em_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PickEmStack(app, "pick-em")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
