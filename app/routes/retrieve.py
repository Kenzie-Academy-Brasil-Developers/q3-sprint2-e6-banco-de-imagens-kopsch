from app.kenzie.image import get_files, get_files_by_extension, extensions
from http import HTTPStatus

def retrieve(app):
    @app.get("/")
    def home():
        return """<h1>Q3</h1>\n
                  <h2>Entrega Banco de imagens</h2>\n"""

    @app.get("/files/<extension>")
    @app.get("/files")
    def getting_files(extension = None):
        if extension is None:
            return get_files()
        elif extension not in extensions:
            return {"message": "Invalid extension"}, HTTPStatus.NOT_FOUND
        else:
            return get_files_by_extension(extension)