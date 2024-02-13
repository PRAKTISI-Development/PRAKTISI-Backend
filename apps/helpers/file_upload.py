from fastapi import UploadFile
from dotenv import load_dotenv
import os
load_dotenv()

def save_uploaded_file(file: UploadFile):
    SERVER_FOLDER = os.getenv("SERVER_FOLDER")
    if not os.path.exists(SERVER_FOLDER):
        os.makedirs(SERVER_FOLDER)

    file_path = os.path.join(SERVER_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path