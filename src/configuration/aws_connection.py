import boto3
import os
from src.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME

class S3Client:

    s3_client = None
    s3_resource = None

    def __init__(self,region_name=REGION_NAME):
        """"
        This class gets aws credentials from env variables and establishes a connectioons3 bucket and
        raise exception when environment variables are missing
        """
        if S3Client.s3_client == None or S3Client.s3_resource==None:
            _access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY,)
            _secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY,)
            if _access_key_id is None:
                raise Exception("Access key ID is missing from the env variable")
            if _secret_access_key is None:
                raise Exception("Secret Access key is missing from the env variable")
            
            S3Client.s3_resource = boto3.resource(
                's3',
                aws_access_key_id = _access_key_id,
                aws_secret_access_key = _secret_access_key,
                region_name = REGION_NAME
            )
            S3Client.s3_client = boto3.resource(
                's3',
                aws_access_key_id = _access_key_id,
                aws_secret_access_key = _secret_access_key,
                region_name = region_name
            )

        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client
