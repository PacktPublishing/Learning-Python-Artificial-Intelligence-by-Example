# Configuring AWS Rekognition

These commands will help you configure AWS for this module.  Note that you'll need to:
 
 * Ensure that you set the relevant regions for your AWS account (mine is `eu-west-1`) 
 * Create `access-policy.json` based on the example file `access-policy-example.json` and add your IAM account 
 ID to line 28 in the DynamoDB config (see below).
 
```json
...{
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:aws-region:account-id:table/applied-ai-collection"
}...               
``` 


## Shell script
If you want to get started quickly, run the command:

```bash
bash configure-aws.sh
```

This will set up all the required services and access policies.  Please make a note of your bucket name which is logged
by the script.



## Manual configuration
If you wish to step through this manually and see exactly what goes on, the following commands will do this for you.

#### Install the AWS CLI
```bash
pip install awscli --upgrade
```

#### Configure the AWS CLI
```bash
aws configure
```

### Rekognition Collection
```bash
aws rekognition create-collection --collection-id applied-ai-collection --region eu-west-1
```

#### DynamoDB
```bash
aws dynamodb create-table --table-name applied-ai-collection \
--attribute-definitions AttributeName=RekognitionId,AttributeType=S \
--key-schema AttributeName=RekognitionId,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
--region eu-west-1
```

#### S3

```bash
aws s3 mb s3://bucket-name --region eu-west-1
```

#### Create the trust policy
```bash
aws iam create-role --role-name LambdaRekognitionRole --assume-role-policy-document file://trust-policy.json

```

#### Attach the access policy
```bash
aws iam put-role-policy --role-name LambdaRekognitionRole --policy-name LambdaPermissions --policy-document file://access-policy.json
```