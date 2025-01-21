from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_ecr_assets as ecr_assets,
    # aws_sqs as sqs,
)
from constructs import Construct
import os 
class MultiAgentsCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        docker_directory = "./docker"
        # example resource
        # queue = sqs.Queue(
        #     self, "MultiAgentsCdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        if not os.path.exists(docker_directory):
            raise FileNotFoundError(f"The specified directory {docker_directory} does not exist.")
        
        # Build Docker image
        asset = ecr_assets.DockerImageAsset(
            self, "Python312Image",
            directory=docker_directory,  # Must be a static, resolvable path
        )


        # Create Lambda function using the container image
        _lambda.Function(
            self, "Python312Function",
            code=_lambda.Code.from_asset_image(asset.image_uri), 
            handler=_lambda.Handler.FROM_IMAGE,
            runtime=_lambda.Runtime.FROM_IMAGE,
        )
