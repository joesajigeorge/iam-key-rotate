# IAM Access Key Rotation

This Python SAM application is to deploy a Lambda function to handle AWS IAM user access key rotation.

    In AWS, you can have a maximum of two access keys per user. 
    Make sure that there is only one access key before executing this program.

## prerequisite

-  Python3.11
-  aws-cli
-  aws-sam-cli

## Deployment

### Build and Validate the application

    sam build
    sam validate

### Deploy the application

    sam deploy --guided

SAM guided deployment will ask you for the stack name, region, parameters. You can also save it to a samconfig.toml file.

### Delete the application

    sam delete
