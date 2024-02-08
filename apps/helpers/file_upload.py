from fastapi import UploadFile
import os

def save_uploaded_file(file: UploadFile):
    upload_folder = "uploads"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path