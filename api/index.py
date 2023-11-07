import os
import shutil
import uuid
import zipfile

from flask import Flask, make_response, request, jsonify

app = Flask(__name__)

import boto3
from botocore.client import Config
import logging
from botocore.exceptions import ClientError

from ApiResponse import ApiResponse
AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
S3_ENDPOINT = 'http://localhost:9444/s3'

bucket_name = 'asd'
object_key = 'object_test1.png'

s3 = boto3.client('s3', endpoint_url=S3_ENDPOINT,
                  aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  config=Config(signature_version='s3v4'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file_zip(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}


@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/get_all_file_names")
def get_all_file_names():
    try:
        objects = s3.list_objects_v2(Bucket=bucket_name)
        file_names = [obj['Key'] for obj in objects.get('Contents', [])]
        return ApiResponse.customResponse(data=file_names, message='success', status=200)
    except Exception as e:
        logging.error('ERRR:', e)
        return ApiResponse.serverError(message=str(e))


@app.route("/api/get_all_files_in_folder")
def get_all_files_in_folder():
    folderName = request.args.to_dict()['folderName']

    try:
        objects = s3.list_objects_v2(Bucket=bucket_name)
        file_names = [obj['Key'] for obj in objects.get('Contents', [])]

        filtered_files = [file for file in file_names if file.startswith(folderName + '/')]
        return ApiResponse.customResponse(data=filtered_files, message='success', status=200)
    except Exception as e:
        logging('Err', e)
        return ApiResponse.serverError(message=str(e))


@app.route("/api/get_all_folder_names")
def get_all_folder_names():
    try:
        objects = s3.list_objects_v2(Bucket=bucket_name)
        file_names = [obj['Key'] for obj in objects.get('Contents', [])]
        folder_names = {file_name.split('/')[0] for file_name in file_names}
        return ApiResponse.customResponse(data=list(folder_names), message='success', status=200)
    except Exception as e:
        logging.error('ERRR:', e)
        return ApiResponse.serverError(message=str(e))


# OOPIFY
@app.route("/api/get_file_by_name")
def get_file_by_name():
    filenameQuery = request.args.to_dict()['filename']
    print('ARGSS: ', filenameQuery)

    try:
        image_data = s3.get_object(Bucket=bucket_name, Key=filenameQuery)['Body'].read()
    except ClientError as e:
        logging.error(e)
        return ApiResponse.serverError(message=str(e))

    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpeg'
    return ApiResponse.customResponse(data=response, message='success', status=200)


@app.route("/api/upload_zip", methods=['POST'])
def upload_zip():
    try:
        uploaded_zip_file = request.files['zipFile']

        if not uploaded_zip_file and not allowed_file_zip(uploaded_zip_file.filename):
            return ApiResponse.customResponse(data=None, message='No file uploaded', status=400)

        folder_name = f'upload-{uuid.uuid4()}'

        extract_dir = './temp'
        os.makedirs(extract_dir, exist_ok=True)
        os.chmod(extract_dir, 0o777)

        zip_file_path = os.path.join(extract_dir, uploaded_zip_file.filename)
        uploaded_zip_file.save(zip_file_path)

        extract_subdir = os.path.join(extract_dir, 'extracted')
        os.makedirs(extract_subdir, exist_ok=True)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_subdir)

        for root, _, files in os.walk(extract_subdir):
            for file in files:
                image_path = os.path.join(root, file)
                object_key_zip = folder_name + '/' + file
                logging.info(f'uploading {object_key_zip}....')
                s3.upload_file(image_path, bucket_name, object_key_zip)

        os.remove(zip_file_path)
        shutil.rmtree('temp')

        logging.info(f'upload successfull {bucket_name}')
        return ApiResponse.customResponse(data=None, message='files uploaded successfully', status=201)

    except Exception as e:
        logging.error('Error: ', e)
        return ApiResponse.serverError(message=str(e))
