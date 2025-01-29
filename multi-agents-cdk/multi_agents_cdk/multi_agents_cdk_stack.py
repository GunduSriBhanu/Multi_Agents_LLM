
from aws_cdk import (
    # Duration,
    Stack,   
    RemovalPolicy, 
    aws_lambda as _lambda,
    aws_ecr_assets as ecr_assets,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_s3 as s3,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    CfnOutput,
    CfnTag,
)
from constructs import Construct
import os 

def write_env_file(env_variables):
    

    # Write the variables to a .env file
    env_file_path = ".env"
    with open(env_file_path, "w") as env_file:
        for key, value in env_variables.items():
            env_file.write(f"{key}={value}\n")

    print(f"\nEnvironment variables successfully written to {os.path.abspath(env_file_path)}")



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

        # Create an S3 bucket
        bucket = s3.Bucket(
            self,
            "Multi_Agents_Storage",
            removal_policy=RemovalPolicy.DESTROY,  # Automatically delete bucket on `cdk destroy`
            auto_delete_objects=True,  # Ensure objects are deleted with the bucket
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable encryption
            bucket_name="multi-agents-storage-custom",
            versioned=True,  # Enable versioning for better data integrity
        )

        # bucket.apply_removal_policy(RemovalPolicy.DESTROY) 

        # Create IAM Role for EC2 instance
        ec2_role = iam.Role(
            self,
            "EC2InstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")  # For SSM access
            ],
        )

        # Add inline policy for S3 read/write access
        ec2_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject",
                    "s3:ListBucket",
                ],
                resources=[
                    bucket.bucket_arn,  # Allow access to the bucket itself
                    f"{bucket.bucket_arn}/*",  # Allow access to all objects in the bucket
                ],
            )
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
            role=ec2_role,  # Attach the IAM role to the EC2 instance           
        )

        # _lambda.DockerImageFunction(
        #     self,
        #     "DockerLambda",
        #     code=_lambda.DockerImageCode.from_image_asset(directory=r"multi_agents_cdk/lambda/python",), #r"multi_agents_cdk\lambda\python"
        #     function_name="DockerLambdaFunction"
        # )   

       

        # Outputs
        CfnOutput(self, "BucketName", value=bucket.bucket_name, description="Name of the S3 bucket")
        CfnOutput(self, "InstanceId", value=instance.instance_id, description="Instance ID of the EC2 instance")
        CfnOutput(
            self, "InstanceRoleArn", value=ec2_role.role_arn, description="IAM Role ARN for the EC2 instance"
        )
        env_variables = {        
        "BUCKET_NAME": bucket.bucket_name,
        "STACK_NAME": "MyCDKStack",
        "InstanceID": instance.instance_id,
        "IP_Address":instance.instance_public_ip
        }
        write_env_file(env_variables)
        


        