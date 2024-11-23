import os


def file_not_found(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f'path "{path}" does not exist')


def unsupported_extension(ext: str, supported: dict):
    if ext not in supported:
        raise AttributeError(f'unsupported extension {ext}')
