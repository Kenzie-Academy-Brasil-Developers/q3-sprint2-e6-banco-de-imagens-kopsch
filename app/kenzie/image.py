from app.kenzie import FILES_DIRECTORY
from zlib import compress
from click import command
from flask import send_file, send_from_directory, jsonify
import os
from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()


path = os.getenv("FILES_DIRECTORY")
limit_size = int(os.getenv("MAX_CONTENT_LENGTH"))
extensions = os.getenv("ALLOWED_EXTENSIONS").split(";")

class FileTooLargeError(Exception):
    default_message = "File too large."
    status_code = 413

    def __init__(self, message=default_message, status_code=status_code):
        self.message = message
        self.status_code = status_code

def verify_file(path) -> bool:
    if(os.path.isfile(path)):
        return True
    return False

def file_already_exists(file, extension) -> bool:
    path = os.path.join(FILES_DIRECTORY, extension)
    return file in os.listdir(path)


def get_files() -> list:
    file_list = []

    for extension in extensions:
        for file in os.listdir(f"{path}/{extension}"):
            pathname = os.path.join(f"{path}/{extension}", file)
            if(verify_file(pathname)):
                file_list.append(file)

    return jsonify(file_list)


def get_files_by_extension(extension) -> list:
    file_list = []

    for file in os.listdir(f"{path}/{extension}"):
        pathname = os.path.join(f"{path}/{extension}", file)
        if(verify_file(pathname)):
            file_list.append(file)

    return jsonify(file_list)


def download_files(file) -> send_from_directory:
    type = file.split(".")[1]
    pathname = os.path.join(f"{path}/{type}", file)
    if not(verify_file(pathname)):
        return {"message": "file not founded"}, HTTPStatus.NOT_FOUND

    return send_from_directory(
        os.path.realpath(f"{path}/{type}"),
        file,
        as_attachment=True
    ), HTTPStatus.OK


def download_zip(ext, compression_ratio) -> str:

    
    file = f"{ext}.zip"
    path = os.path.join(FILES_DIRECTORY, ext)
    file_path = os.path.join("/tmp", file)
    
    if verify_file(file_path):
        os.remove(file_path)

    task = f'zip -r -j -{compression_ratio} {file_path} {path}'
    os.system(task)

    return send_file(file_path, as_attachment=True)


def upload_image(file: FileStorage) -> None or dict:
    filename = file.filename
    _, ext = os.path.splitext(filename)
    ext = ext.replace(".", "")

    if file_already_exists(filename, ext):
        raise FileExistsError

    path = os.path.join(FILES_DIRECTORY, ext, filename)
    file.save(path)
    file_size = os.stat(path).st_size
    
    if file_size > limit_size:
        os.remove(path)
        raise FileTooLargeError