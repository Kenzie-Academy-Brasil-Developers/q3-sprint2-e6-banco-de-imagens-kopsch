from app.routes.retrieve import retrieve
from app.routes.upload import upload
from app.routes.download import download

def init_app(app):
    retrieve(app)
    upload(app)
    download(app)