import aws_cdk as core
import aws_cdk.assertions as assertions

from multi_agents_cdk.multi_agents_cdk_stack import MultiAgentsCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in multi_agents_cdk/multi_agents_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MultiAgentsCdkStack(app, "multi-agents-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
