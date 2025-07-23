import os
import shutil

from functools import wraps


def list_directory(dirname: str) -> list[str]:
    items = sorted(os.listdir(dirname))
    return [os.path.join(dirname, item) for item in items]


def remove_temp_directory():
    if os.path.exists("_temp"):
        shutil.rmtree("_temp")


def process_path(path: str) -> list[str]:
    paths = []

    if not os.path.exists(path):
        paths.append(path)

    if os.path.isfile(path):
        paths.append(path)

    if os.path.isdir(path):
        paths.extend(list_directory(path))

    return paths


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            remove_temp_directory()
            exit(f'error: {str(e)}')

    return wrapper
