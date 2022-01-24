from http import HTTPStatus
from flask import request
from app.kenzie.image import download_files, download_zip


def download(app):
    @app.get("/download/<file>")
    def download_file(file):
        return download_files(file)

    @app.get("/download-zip")
    def download_zip_files():
        ext = request.args.get("file_extension")
        compression_ratio = request.args.get("compression_ratio")

        if not ext:
            return {"message": "You must specify the extension in query params"}, HTTPStatus.BAD_REQUEST
        download_zip(ext, compression_ratio)
        return {"message": "zip archive successfully downloaded"}, HTTPStatus.OK