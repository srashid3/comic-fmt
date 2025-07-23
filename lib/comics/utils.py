import os


def num_digits(num: int):
    return len(str(num))


def zero_padded(cnt: int):
    return f'0{num_digits(cnt)}'


def sanitize_extension(ext: str) -> str:
    return "." + ext.replace(".", "").strip()


def get_file_extension(path: str) -> str:
    return os.path.splitext(path)[1] or ""


def remove_file_extension(path: str) -> str:
    return os.path.splitext(path)[0]


def change_file_extension(path: str, ext: str) -> str:
    return f'{remove_file_extension(path)}{sanitize_extension(ext)}'


def remove_top_directory(path: str) -> str:
    return path.split(os.path.sep, 1)[-1]


def traverse(dirname: str):
    for item in sorted(os.listdir(dirname)):
        path = os.path.join(dirname, item)

        if os.path.isdir(path):
            yield from traverse(path)

        yield dirname, item
