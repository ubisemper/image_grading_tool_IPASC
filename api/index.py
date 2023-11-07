import os
import logging

from dotenv import load_dotenv
from botocore.exceptions import ClientError
from flask import Flask, make_response, request, jsonify

from services.S3StorageService import S3StorageService
from services.ZipperService import ZipAndUploadService
from utils.Sanitation import allowed_file_zip
from ApiResponse import ApiResponse
from sqlTest import Database

# SERVER CONFIGURATION STEPS
app = Flask(__name__)
load_dotenv()
logging.basicConfig(level=logging.INFO)

db_url = 'sqlite:///test.sqlite'
db = Database(db_url)
db.create_all()


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
        logging.error('Error:', e)
        return ApiResponse.serverError(message=str(e))
    

@app.route("/api/get_all_folder_names")
def get_all_folder_names():
    try:
        folder_names = s3_storage_service.get_all_folder_names()
        return ApiResponse.customResponse(data=list(folder_names), message='success', status=200)
    except Exception as e:
        logging.error('Error:', e)
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
        
        zipper = ZipAndUploadService(s3_storage_service)
        zipper.process_zip_file(uploaded_zip_file)

        logging.info(f'upload successful')
        return ApiResponse.customResponse(data=None, message='files uploaded successfully', status=201)

    except Exception as e:
        logging.error('Error: ', e)
        return ApiResponse.serverError(message=str(e))
    

# TODO Check if file is valid or not
@app.route("/api/grade_image")
def grade_image():
    fileName = request.args.to_dict()['fileName']
    user = request.args.to_dict()['user']
    grade = request.args.to_dict()['grade']

    try:
        db.add_grade(fileName, user, int(grade))
        return ApiResponse.customResponse(data=None, message='grade uploaded successfully', status=201)
    except Exception as e:
        return ApiResponse.serverError(message=str(e))