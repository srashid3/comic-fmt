import pytest

from unittest.mock import MagicMock
from unittest.mock import patch

from comics import Archive


def mock_context_manager():
    mocked_class = MagicMock()
    mocked_context = MagicMock()

    mocked_context_manager = mocked_class.return_value
    mocked_context_manager.__enter__.return_value = mocked_context

    return mocked_class, mocked_context


@pytest.fixture(autouse=True)
def setup_file_system(fs):
    fs.create_dir("test_dir")

    fs.create_file("test.rar")

    fs.create_file("test_dir/test.zip")
    fs.create_file("test_dir/test_1.jpg")
    fs.create_file("test_dir/test_2.jpg")
    fs.create_file("test_dir/test_3.jpg")


@pytest.fixture
def zip_archive():
    target = "comics.archive.supported_extensions"

    zip_file, zip_archive = mock_context_manager()

    zip_archive.namelist.return_value = [
        "test_1.jpg", "test_2.jpg", "test_3.jpg"
    ]

    with patch.dict(target, {".zip": zip_file}):
        yield zip_archive


@pytest.fixture
def rar_archive():
    target = "comics.archive.supported_extensions"

    rar_file, rar_archive = mock_context_manager()

    rar_archive.namelist.return_value = [
        "test_1.jpg", "test_2.jpg", "test_3.jpg"
    ]

    with patch.dict(target, {".rar": rar_file}):
        yield rar_archive


def test_file():
    a = Archive("test.rar")

    assert a.path == "test.rar"
    assert a.dirname == ""
    assert a.filename == "test.rar"
    assert a.ext == ".rar"


def test_dir():
    a = Archive("test_dir/test.zip")

    assert a.path == "test_dir/test.zip"
    assert a.dirname == "test_dir"
    assert a.filename == "test.zip"
    assert a.ext == ".zip"


def test_invalid_path():
    with pytest.raises(FileNotFoundError):
        Archive("missing_file")


def test_unsupported_extension():
    with pytest.raises(AttributeError):
        Archive("test_dir/test_1.jpg")


def test_compress(zip_archive, rar_archive):
    Archive.compress("test_dir", "new.zip")

    zip_archive.write.assert_called()
    rar_archive.write.assert_not_called()

    expected_items = ["test_1.jpg", "test_2.jpg", "test_3.jpg"]

    for item in expected_items:
        zip_archive.write.assert_any_call(
            f'test_dir/{item}',
            arcname=None
        )


def test_uncompress(zip_archive, rar_archive):
    a = Archive("test.rar")

    a.uncompress()

    zip_archive.extractall.assert_not_called()
    rar_archive.extractall.assert_called()


def test_search(rar_archive):
    a = Archive("test.rar")

    results = a.search("test")
    assert len(results) == 3

    assert results[0] == "test_1.jpg"
    assert results[1] == "test_2.jpg"
    assert results[2] == "test_3.jpg"

    results = a.search("missing")
    assert len(results) == 0
