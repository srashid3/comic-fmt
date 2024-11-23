import pytest

from comics import handler


def test_file_not_found():
    handler.file_not_found(__file__)

    with pytest.raises(FileNotFoundError):
        handler.file_not_found("missing_file")


def test_unsupported_extension():
    supported = [".zip", ".rar"]

    handler.unsupported_extension(".zip", supported)

    with pytest.raises(AttributeError):
        handler.unsupported_extension(".jpg", supported)
