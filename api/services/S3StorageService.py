from services.StorageService import StorageService
from botocore.client import Config
from botocore.exceptions import ClientError
import logging
import boto3

class S3StorageService(StorageService):
    def __init__(self, credentials):
        self.s3 = boto3.client('s3', endpoint_url=credentials['end_point_url'],
                  aws_access_key_id=credentials['access_key'],
                  aws_secret_access_key=credentials['secret_key'],
                  config=Config(signature_version='s3v4'))  
        
        self.bucket_name = credentials['bucket_name']

    def get_all_file_names(self):
        try:
            objects = self.s3.list_objects_v2(Bucket=self.bucket_name)
            file_names = [obj['Key'] for obj in objects.get('Contents', [])]
            logging.info('file names successfully retrieved')
            return file_names
        except ClientError as e:
            logging.error('Error: ', str(e))
            return e
        
    def get_all_folder_names(self):
        file_names = self.get_all_file_names()
        folder_names = {file_name.split('/')[0] for file_name in file_names}
        return folder_names

    def get_file_names_in_folder(self, folder_name):
        file_names = self.get_all_file_names()
        filtered_file_names = [file for file in file_names if file.startswith(folder_name + '/')]
        return filtered_file_names
    
    def get_file_by_name(self, file_name):
        try:
            file = self.s3.get_object(Bucket=self.bucket_name, Key=file_name)['Body'].read()
            logging.info('file successfully retrieved')
            return file
        except ClientError as e:
            logging.error('Error: ', str(e))
            return e
        
    def upload_file(self, image_path, object_key):
        try:
            self.s3.upload_file(image_path, self.bucket_name, object_key)
            return True
        except ClientError as e:
            logging.error('Error: ', str(e))
            return False
        