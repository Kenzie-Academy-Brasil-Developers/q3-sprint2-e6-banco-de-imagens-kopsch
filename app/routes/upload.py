from http import HTTPStatus
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from flask import request
from app.kenzie.image import FileTooLargeError, upload_image, limit_size

def upload(app):
    @app.post("/upload")
    def post_image():
        files: ImmutableMultiDict[str, FileStorage] = request.files
        for file in files.values():
            try:
                upload_image(file)
                    
            except FileExistsError:
                return {"message": "File already exists"}, HTTPStatus.CONFLICT
            except FileNotFoundError:
                return {"message": "Extension not supported"}, HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            except FileTooLargeError as e:
                return {"message": e.message}, e.status_code
            return {"message": "File has been uploaded"}, HTTPStatus.CREATED