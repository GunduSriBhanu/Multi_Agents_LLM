ifneq (,$(wildcard .env))
include .env
export $(shell sed 's/=.*//' .env)
endif

# Variables
BUCKET_NAME = my-s3-bucket
REGION = $(CDK_DEFAULT_REGION)
STACK_NAME = MyCDKStack
InstanceID = i-0ead661d7d67a4aca

# S3 Targets
s3-list:
	@echo "Listing S3 buckets in region $(REGION)..."
	aws s3 ls

s3-sync-upload:
	@echo "Uploading files to S3 bucket $(BUCKET_NAME)..."
	aws s3 sync ./data s3://$(BUCKET_NAME)

s3-sync-download:
	@echo "Downloading files from S3 bucket $(BUCKET_NAME)..."
	aws s3 sync s3://$(BUCKET_NAME) ./data

# CDK Targets
cdk-bootstrap:
	@echo "Bootstrapping CDK environment in region $(REGION)..."
	cdk bootstrap

cdk-synth:
	@echo "Synthesizing CloudFormation template for the stack $(STACK_NAME)..."
	cdk synth

cdk-deploy:
	@echo "Deploying the stack $(STACK_NAME)..."
	cdk deploy --require-approval never

cdk-destroy:
	@echo "Destroying the stack $(STACK_NAME)..."
	cdk destroy --force

cdk-diff:
	@echo "Checking differences between deployed stack and current code..."
	cdk diff

# SSH into EC2 instance using InstanceID
ssh-ec2:
	@echo "Connecting to EC2 instance with ID $(InstanceID)..."
	aws ec2-instance-connect ssh --instance-id $(InstanceID)

# Environment Check
# check-env:
# 	@echo "AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID)"
# 	@echo "AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY)"
# 	@echo "AWS_DEFAULT_REGION=$(CDK_DEFAULT_REGION)"
# 	@echo "InstanceID=$(InstanceID)"

# Target to display all environment variables in the .env file
check-env:
	@if exist .env ( \
		echo Environment variables in the .env file: && \
		type .env \
	) else ( \
		echo .env file not found! \
	)

# Target to update a specific environment variable
update-env:
	@echo "Updating environment variable $(VARIABLE_NAME) in .env..."
	@sed -i.bak "s/^$(VARIABLE_NAME)=.*/$(VARIABLE_NAME)=$(NEW_VALUE)/" .env || echo "$(VARIABLE_NAME)=$(NEW_VALUE)" >> .env
	@echo "$(VARIABLE_NAME) updated to $(NEW_VALUE)"

# Target to add a new environment variable
add-env:
	@echo "Adding environment variable $(VARIABLE_NAME) to .env..."
	@powershell -Command "if (!(Select-String -Path .env -Pattern '^$(VARIABLE_NAME)=.*')) { \
		Add-Content .env -Value \"$(VARIABLE_NAME)=$(NEW_VALUE)`n\"; \
		Write-Host '$(VARIABLE_NAME) added with value $(NEW_VALUE)'; \
	} else { \
		Write-Host '$(VARIABLE_NAME) already exists in .env'; \
	}"


# Cleanup (optional)
cleanup:
	@echo "Cleaning up generated files and folders..."
	rm -rf cdk.out .aws-sam build .pytest_cache

# Help target
help:
	@echo "Available targets:"
	@echo "  make s3-list           - List all S3 buckets"
	@echo "  make s3-sync-upload    - Upload files from ./data to the S3 bucket"
	@echo "  make s3-sync-download  - Download files from the S3 bucket to ./data"
	@echo "  make cdk-bootstrap     - Bootstrap the CDK environment"
	@echo "  make cdk-synth         - Synthesize the CloudFormation template"
	@echo "  make cdk-deploy        - Deploy the CDK stack"
	@echo "  make cdk-destroy       - Destroy the CDK stack"
	@echo "  make cdk-diff          - View changes between deployed and current code"
	@echo "  make ssh-ec2           - SSH into EC2 instance with the given InstanceID"
	@echo "  make check-env         - Display loaded environment variables"
	@echo "  make cleanup           - Remove generated files and folders"
	@echo "  make update-env VARIABLE_NAME=<name> NEW_VALUE=<value> - Update an environment variable in .env"
	@echo "  make add-env VARIABLE_NAME=<name> NEW_VALUE=<value> - Add a new environment variable to .env"
