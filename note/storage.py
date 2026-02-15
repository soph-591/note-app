import os
from flask import current_app

def save_upload(file, uuid, name):
    filename = f"{uuid}_{name}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    return file

def load_upload(uuid, name):
    filename = f"{uuid}_{name}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    with open(path, encoding="utf-8") as f:
        return f.read()
