from api.dataModels import Database, Grade, Folder, Image
import os
from dotenv import load_dotenv
import shutil

import logging

from services.S3StorageService import S3StorageService


logging.basicConfig(level=logging.INFO)
load_dotenv()
db_url = "sqlite:///test.sqlite"
db = Database(db_url)

s3_credentials = {
    "access_key": os.getenv("AWS_ACCESS_KEY"),
    "secret_key": os.getenv("AWS_SECRET_KEY"),
    "end_point_url": os.getenv("S3_ENDPOINT"),
    "bucket_name": os.getenv("BUCKET_NAME"),
}


def get_classes():
    session = db.create_session()
    result = session.query(Grade.grade).distinct().all()
    session.close()
    return [str(item[0]) for item in result]


def get_names_and_grades_in_folder(folder_name):
    session = db.create_session()

    result = (
        session.query(Image.filename, Grade.grade)
        .join(Grade, Image.filename == Grade.image_id)
        .join(Folder, Image.folder_id == Folder.id)
        .filter(Grade.folder_name == folder_name, Folder.foldername == folder_name)
        .all()
    )

    session.close()
    return result


def create_folders():
    data_dir = "data"
    folder_names = get_classes()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    for folder_name in folder_names:
        os.makedirs(os.path.join(data_dir, folder_name), exist_ok=True)


def process_images(folder):
    create_folders()
    s3 = S3StorageService(s3_credentials)
    images = get_names_and_grades_in_folder(folder)

    # Retrieve image from S3
    for image in images:
        image_data = s3.get_file_by_name(os.path.join(folder, image[0]))
        # Save image to corresponding folder with ID
        folder_name = str(image[1])
        data_dir = "data"
        file_path = os.path.join(data_dir, folder_name, image[0])
        with open(file_path, "wb") as f:
            f.write(image_data)

    shutil.make_archive(f"images_zipped/{folder}", "zip", "data")
    shutil.rmtree("data")
    return f"images_zipped/{folder}"
