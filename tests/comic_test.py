import os
import pytest

from unittest.mock import MagicMock
from unittest.mock import patch

from comics import Comic


def create_file(path):
    dirname = os.path.dirname(path)

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    with open(path, 'w'):
        pass


def mock_uncompress(items=None):
    items = items or []

    def func(output_path):
        os.mkdir(output_path)

        for item in items:
            create_file(os.path.join(output_path, item))

    return func


@pytest.fixture(autouse=True)
def setup_file_system(fs):
    fs.create_file("test.cbr")
    fs.create_file("test.cbz")


def test_edit():
    c = Comic("test.cbz")

    c.archive = MagicMock()
    c.edit()

    assert c._Comic__edit_mode is True
    c.archive.uncompress.assert_called()


def test_save():
    c = Comic("test.cbz")

    c.archive.uncompress = mock_uncompress()
    c.edit()

    assert c._Comic__edit_mode is True
    assert os.path.exists("_temp")

    c.save()

    assert c._Comic__edit_mode is False
    assert not os.path.exists("_temp")


def test_rename():
    c = Comic("test.cbz")

    c.rename()
    assert c.title == "test"

    c.rename(title="Hello World (2024) [Test]")
    assert c.title == "Hello World (2024) [Test]"

    c.rename(cleanup=True)
    assert c.title == "Hello World"


def test_search():
    c = Comic("test.cbz")

    c.archive = MagicMock()
    c.search("test")

    c.archive.search.assert_called_with("test")


def test_uncompress():
    c = Comic("test.cbr")

    c.archive = MagicMock()
    c.uncompress()

    c.archive.uncompress.assert_called()


def test_convert_cbr():
    c = Comic("test.cbr")

    c.archive.uncompress = mock_uncompress()
    c.convert()

    assert os.path.exists("test.cbz")

    assert not os.path.exists("_temp")
    assert not os.path.exists("test.cbr")


def test_convert_cbz():
    c = Comic("test.cbz")

    c.archive.uncompress = mock_uncompress
    c.convert()

    assert not os.path.exists("_temp")
    assert os.path.exists("test.cbz")


def test_flatten():
    c = Comic("test.cbr")

    items = ["test_1.jpg", "dir_1/test_2.jpg", "dir_2/test_3.jpg"]

    c.archive.uncompress = mock_uncompress(items)
    c.flatten()

    assert c._Comic__edit_mode is True

    with patch("shutil.rmtree"):
        c.save()

    assert os.path.exists("test.cbz")
    assert not os.path.exists("test.cbr")

    assert not os.path.exists("_temp/dir_1")
    assert not os.path.exists("_temp/dir_2")

    assert os.path.exists("_temp/test_1.jpg")
    assert os.path.exists("_temp/test_2.jpg")
    assert os.path.exists("_temp/test_3.jpg")


def test_format_pages():
    c = Comic("test.cbr")

    items = ["test_1.jpg", "test_2.jpg", "test_3.jpg"]

    c.archive.uncompress = mock_uncompress(items)
    c.format_pages(page_name="Page ", page_regex=r"\d+")

    assert c._Comic__edit_mode is True

    with patch("shutil.rmtree"):
        c.save()

    assert os.path.exists("test.cbz")
    assert not os.path.exists("test.cbr")

    assert os.path.exists("_temp/Page 1.jpg")
    assert os.path.exists("_temp/Page 2.jpg")
    assert os.path.exists("_temp/Page 3.jpg")


def test_format_pages_recursive():
    c = Comic("test.cbz")

    items = [
        "dir_1/test_2.jpg",
        "dir_1/test_4.jpg",
        "dir_2/test_6.jpg",
        "dir_2/test_8.jpg"
    ]

    c.archive.uncompress = mock_uncompress(items)
    c.format_pages(page_name="Page ", page_regex=r"\d+")

    with patch("shutil.rmtree"):
        c.save()

    assert os.path.exists("_temp/dir_1/Page 1.jpg")
    assert os.path.exists("_temp/dir_1/Page 2.jpg")

    assert os.path.exists("_temp/dir_2/Page 1.jpg")
    assert os.path.exists("_temp/dir_2/Page 2.jpg")


def test_format_pages_remove():
    c = Comic("test.cbz")

    items = [
        "test.xml",
        "test_1.jpg",
        "test_2.jpg",
        "test_3.jpg",
        "credits.jpg"
    ]

    c.archive.uncompress = mock_uncompress(items)
    c.format_pages(page_name="Page ", page_regex=r"\d+", remove=True)

    with patch("shutil.rmtree"):
        c.save()

    assert not os.path.exists("_temp/test.xml")
    assert not os.path.exists("_temp/credits.jpg")

    assert os.path.exists("_temp/Page 1.jpg")
    assert os.path.exists("_temp/Page 2.jpg")
    assert os.path.exists("_temp/Page 3.jpg")
