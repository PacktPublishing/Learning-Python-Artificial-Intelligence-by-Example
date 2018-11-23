#!/usr/bin/env bash

# Get region
DEFAULT_REGION="eu-west-1"
read -e -p "Please enter your AWS region [${DEFAULT_REGION}]:" REGION
REGION="${REGION:-${DEFAULT_REGION}}"

# Get collection name
COLLECTION="applied-ai-collection"

# Table name
TABLE_NAME="applied-ai-collection"

# Buckets need to be unique across AWS, so loop until one is created
DEFAULT_BUCKET_NAME="applied-ai-`date +"%Y%m%d%H%M%S"`"
read -e -p "Please enter your S3 bucket name [${DEFAULT_BUCKET_NAME}]:" BUCKET_NAME
BUCKET_NAME="${BUCKET_NAME:-${DEFAULT_BUCKET_NAME}}"

# Now install AWS CLI and configure
pip install awscli --upgrade && \
aws configure && \
aws rekognition create-collection --collection-id ${COLLECTION} --region ${REGION} && \
aws dynamodb create-table --table-name ${TABLE_NAME} \
--attribute-definitions AttributeName=RekognitionId,AttributeType=S \
--key-schema AttributeName=RekognitionId,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
--region ${REGION} && \

# Create an AWS Bucket
aws s3 mb s3://${BUCKET_NAME} --region ${REGION} && \

# Create the trust policy
aws iam create-role --role-name LambdaRekognitionRole --assume-role-policy-document file://trust-policy.json && \

# Attach the access policy
aws iam put-role-policy --role-name LambdaRekognitionRole --policy-name LambdaPermissions --policy-document file://access-policy.json && \

# Exit with important information
echo "Created S3 bucket with unique name ${BUCKET_NAME}"
echo "\nAWS Configuration completed"
exit 0
