from http import HTTPStatus
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from flask import request
from app.kenzie.image import upload_image, limit_size

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
            return {"message": "File has been uploaded"}, HTTPStatus.CREATED
        
    @app.errorhandler(413)
    def size_exceeded(error):
        return {"message": "Size limit of {limit_size} exceeded"}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE