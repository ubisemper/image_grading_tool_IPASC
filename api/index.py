import os
import logging

from dotenv import load_dotenv
from botocore.exceptions import ClientError
from flask import Flask, make_response, request, send_file
from celery import Celery

from services.S3StorageService import S3StorageService
from services.ZipperService import ZipAndUploadService
from utils.Sanitation import allowed_file_zip
from ApiResponse import ApiResponse
from dataModels import Database

# from sqlQueries import process_images
from services.datasetService import datasetService

# SERVER CONFIGURATION STEPS

app = Flask(__name__)
load_dotenv()
logging.basicConfig(level=logging.DEBUG)

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)

db_url = "sqlite:///test.sqlite"
db = Database(db_url)
db.create_all()


s3_credentials = {
    "access_key": os.getenv("AWS_ACCESS_KEY"),
    "secret_key": os.getenv("AWS_SECRET_KEY"),
    "end_point_url": os.getenv("S3_ENDPOINT"),
    "bucket_name": os.getenv("BUCKET_NAME"),
}

s3_storage_service = S3StorageService(s3_credentials)
dataset_service = datasetService(db, s3_credentials)


@app.route("/api/trigger_zip")
def trigger_zip():
    folder_name = request.args.to_dict()["folderName"]
    task = create_dataset.delay(folder_name)
    return ApiResponse.customResponse(
        data=str(task.id), message="Task started", status=202
    )


@celery.task
def create_dataset(folder_name):
    # return process_images(folder_name)
    return dataset_service.process_images(folder_name)


@app.route("/api/download/<task_id>")
def download(task_id):
    result = celery.AsyncResult(task_id)
    if result.successful():
        zip_file_path = result.get()
        return send_file(zip_file_path, as_attachment=True)
    else:
        return "Task not completed yet"


@app.route("/api/get_all_file_names")
def get_all_file_names():
    try:
        file_names = s3_storage_service.get_all_file_names()
        return ApiResponse.customResponse(
            data=file_names, message="success", status=200
        )
    except Exception as e:
        logging.error("Error:", e)
        return ApiResponse.serverError(message=str(e))


@app.route("/api/get_all_folder_names")
def get_all_folder_names():
    try:
        folder_names = s3_storage_service.get_all_folder_names()
        return ApiResponse.customResponse(
            data=list(folder_names), message="success", status=200
        )
    except Exception as e:
        logging.error("Error:", e)
        return ApiResponse.serverError(message=str(e))


# TODO: Input sanitation
@app.route("/api/get_all_files_in_folder")
def get_all_files_in_folder():
    folderName = request.args.to_dict()["folderName"]

    try:
        filtered_file_names = s3_storage_service.get_file_names_in_folder(folderName)
        return ApiResponse.customResponse(
            data=filtered_file_names, message="success", status=200
        )
    except Exception as e:
        logging("Err", e)
        return ApiResponse.serverError(message=str(e))


@app.route("/api/get_file_by_name")
def get_file_by_name():
    try:
        filenameQuery = request.args.to_dict()["filename"]
        image_data = s3_storage_service.get_file_by_name(filenameQuery)
    except ClientError as e:
        logging.error(e)
        return ApiResponse.serverError(message=str(e))

    response = make_response(image_data)
    response.headers["Content-Type"] = "image/jpeg"
    return response, 200


@app.route("/api/upload_zip", methods=["POST"])
def upload_zip():
    try:
        uploaded_zip_file = request.files["zipFile"]

        if not uploaded_zip_file and not allowed_file_zip(uploaded_zip_file.filename):
            return ApiResponse.customResponse(
                data=None, message="No file uploaded", status=400
            )

        zipper = ZipAndUploadService(db, s3_storage_service)
        zipper.process_zip_file(uploaded_zip_file)

        logging.info(f"upload successful")
        return ApiResponse.customResponse(
            data=None, message="files uploaded successfully", status=201
        )

    except Exception as e:
        logging.error("Error: ", e)
        return ApiResponse.serverError(message=str(e))


# TODO Check if file is valid or not
@app.route("/api/grade_image")
def grade_image():
    fileName = request.args.to_dict()["fileName"]
    folder_name, fileName = fileName.split("/")
    grade = request.args.to_dict()["grade"]

    try:
        db.add_grade(fileName, folder_name, int(grade))
        return ApiResponse.customResponse(
            data=None, message="grade uploaded successfully", status=201
        )
    except Exception as e:
        return ApiResponse.serverError(message=str(e))


@app.route("/start_zip", methods=["POST"])
def start_zip():
    pass


@app.route("/get_zip/<task_id>", methods=["GET"])
def get_zip(task_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5328, host="0.0.0.0")
