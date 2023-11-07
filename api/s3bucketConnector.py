import boto3
from botocore.client import Config
import logging
from botocore.exceptions import ClientError

AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
S3_ENDPOINT = 'http://localhost:9444/s3'

if __name__ == "__main__":
    s3 = boto3.client('s3', endpoint_url=S3_ENDPOINT,
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY,
                      config=Config(signature_version='s3v4'))

    bucket_name = 'asd'
    file_path = '../../../PA images/1-PA.png'
    object_key = 'object_test1.png'

    try:
        s3.upload_file(file_path, bucket_name, object_key)
        logging.info('upload success')
    except ClientError as e:
        logging.error(e)

    try:
        with open('object_test1.png', 'wb') as f:
            s3.download_fileobj(bucket_name, object_key, f)
    except ClientError as e:
        logging.error(e)
