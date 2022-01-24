import os

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

def manage_files() -> None:
    for extension in ALLOWED_EXTENSIONS.split(";"):
        path = os.path.join(FILES_DIRECTORY, extension)
        if not os.path.exists(path):
            os.makedirs(path)
            
manage_files()