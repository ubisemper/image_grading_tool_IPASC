from celery import Celery
from flask import Flask, jsonify, send_file
import zipfile
import os
import datetime

app = Flask(__name__)

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
)


@app.route("/")
def hello():
    task = zip_images.delay()
    return jsonify({"task_id": str(task.id), "status": "Task started"}), 202


@app.route("/download/<task_id>")
def download(task_id):
    result = celery.AsyncResult(task_id)
    if result.successful():
        zip_file_path = result.get()
        return send_file(zip_file_path, as_attachment=True)
    else:
        return "Task not completed yet"


@celery.task
def zip_images():
    image_dir = "./images"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_file_path = f"./images_zipped/images_{current_time}.zip"

    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        for root, _, files in os.walk(image_dir):
            for file in files:
                if file.endswith(".jpg") or file.endswith(
                    ".png"
                ):  # add more conditions if you have other image types
                    zipf.write(os.path.join(root, file), arcname=file)

    return zip_file_path


# Use task ID to get the file
# Check if objects don't get very big if it takes all from a single task object,
# or that it gets garbaged collected
