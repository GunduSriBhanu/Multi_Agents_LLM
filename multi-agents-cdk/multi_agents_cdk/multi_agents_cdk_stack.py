from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_ecr_assets as ecr_assets,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    CfnOutput,
    CfnTag,
)
from constructs import Construct
import os 
class MultiAgentsCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Basic VPC
        vpc = ec2.Vpc(
            self,
            "MyVpc",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-subnet-1",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                )
            ],
        )

        # Create Security Group
        sec_group = ec2.SecurityGroup(
            self,
            "MySecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,  # Allow all outbound traffic
        )

        # Add Ingress Rule for SSH (Port 22)
        sec_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),  # Allow traffic from any IPv4 address
            ec2.Port.tcp(22),     # Port 22 for SSH
            "Allow SSH access"
        )

        # Add Ingress Rule for Port 8000 (Custom Application)
        sec_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),  # Allow traffic from any IPv4 address
            ec2.Port.tcp(8000),   # Port 8000
            "Allow access to port 8000 from anywhere"
        )

        # Create Key Pair
        cfn_key_pair = ec2.CfnKeyPair(
            self,
            "MyCfnKeyPair",
            key_name="cdk-ec2-key-pair-med",
            tags=[CfnTag(key="key", value="value")],
        )

        # Create EC2 Instance with Amazon Linux 2023 AMI
        instance = ec2.Instance(
            self,
            "MyInstance",
            instance_type=ec2.InstanceType("t2.medium"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            security_group=sec_group,
            associate_public_ip_address=True,
            key_name=cfn_key_pair.key_name,
        )

        # Output the Instance ID
        CfnOutput(
            self, "InstanceId",
            value=instance.instance_id,
            description="Instance ID of the created EC2 instance",
        )

        _lambda.DockerImageFunction(
            self,
            "DockerLambda",
            code=_lambda.DockerImageCode.from_image_asset(r"multi_agents_cdk\lambda\python"),
            function_name="DockerLambdaFunction"
        )