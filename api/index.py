import os
import shutil
import uuid
import zipfile
import logging

from dotenv import load_dotenv
from botocore.exceptions import ClientError
from flask import Flask, make_response, request, jsonify

from services.S3StorageService import S3StorageService
from ApiResponse import ApiResponse
from utils.Sanitation import allowed_file_zip




# SERVER CONFIGURATION STEPS
app = Flask(__name__)
load_dotenv()
logging.basicConfig(level=logging.INFO)

s3_credentials = {
    'access_key': os.getenv('AWS_ACCESS_KEY'),
    'secret_key': os.getenv('AWS_SECRET_KEY'),
    'end_point_url': os.getenv('S3_ENDPOINT'),
    'bucket_name': os.getenv('BUCKET_NAME'),
}

s3_storage_service = S3StorageService(s3_credentials)


@app.route("/api/get_all_file_names")
def get_all_file_names():
    try:
        file_names = s3_storage_service.get_all_file_names()
        return ApiResponse.customResponse(data=file_names, message='success', status=200)
    except Exception as e:
        logging.error('ERRR:', e)
        return ApiResponse.serverError(message=str(e))
    

@app.route("/api/get_all_folder_names")
def get_all_folder_names():
    try:
        folder_names = s3_storage_service.get_all_folder_names()
        return ApiResponse.customResponse(data=list(folder_names), message='success', status=200)
    except Exception as e:
        logging.error('ERRR:', e)
        return ApiResponse.serverError(message=str(e))


# TODO: Input sanitation
@app.route("/api/get_all_files_in_folder")
def get_all_files_in_folder():
    folderName = request.args.to_dict()['folderName']

    try:
        filtered_file_names = s3_storage_service.get_file_names_in_folder(folderName)
        return ApiResponse.customResponse(data=filtered_file_names, message='success', status=200)
    except Exception as e:
        logging('Err', e)
        return ApiResponse.serverError(message=str(e))


@app.route("/api/get_file_by_name")
def get_file_by_name():
    try:
        filenameQuery = request.args.to_dict()['filename']
        image_data = s3_storage_service.get_file_by_name(filenameQuery)
    except ClientError as e:
        logging.error(e)
        return ApiResponse.serverError(message=str(e))

    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpeg'
    return response, 200


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
                s3_storage_service.upload_file(image_path, object_key_zip)

        os.remove(zip_file_path)
        shutil.rmtree('temp')

        logging.info(f'upload successful')
        return ApiResponse.customResponse(data=None, message='files uploaded successfully', status=201)

    except Exception as e:
        logging.error('Error: ', e)
        return ApiResponse.serverError(message=str(e))
