import os
import shutil
import zipfile
import uuid
import logging

# TODO: File checker

class ZipAndUploadService:
    def __init__(self, storage_service, extract_dir='./temp'):
        self.storage_service = storage_service
        self.extract_dir = extract_dir
    
    def process_zip_file(self, uploaded_zip_file):
         folder_name = f'upload-{uuid.uuid4()}'

         os.makedirs(self.extract_dir, exist_ok=True)
         os.chmod(self.extract_dir, 0o777)

         zip_file_path = os.path.join(self.extract_dir, uploaded_zip_file.filename)
         uploaded_zip_file.save(zip_file_path)

        # To prefent the zipfile itself to get uploaded, we extract the zip file in a subdirectory
         extract_subdir = os.path.join(self.extract_dir, 'extracted')
         os.makedirs(extract_subdir, exist_ok=True)

         with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_subdir)

         for root, _, files in os.walk(extract_subdir):
             for file in files:
                 image_path = os.path.join(root, file)
                 object_key_zip = folder_name + '/' + file
                 logging.info(f'uploading {object_key_zip}....')
                 self.storage_service.upload_file(image_path, object_key_zip)

         os.remove(zip_file_path)
         shutil.rmtree('temp')