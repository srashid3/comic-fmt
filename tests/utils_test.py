from comics import utils


def test_num_digits():
    assert utils.num_digits(1) == 1
    assert utils.num_digits(10) == 2
    assert utils.num_digits(100) == 3


def test_zero_padded():
    assert utils.zero_padded(1) == "01"
    assert utils.zero_padded(10) == "02"
    assert utils.zero_padded(100) == "03"


def test_sanitize_extension():
    extensions = ["zip", ".zip", "..zip", " .zip "]

    for ext in extensions:
        assert utils.sanitize_extension(ext) == ".zip"


def test_get_file_extension():
    assert utils.get_file_extension("test.rar") == ".rar"
    assert utils.get_file_extension("no_extension") == ""


def test_remove_file_extension():
    assert utils.remove_file_extension("test.zip") == "test"
    assert utils.remove_file_extension("no_extension") == "no_extension"


def test_change_file_extension():
    assert utils.change_file_extension("test.cbr", "cbz") == "test.cbz"
    assert utils.change_file_extension("new", "cbz") == "new.cbz"


def test_remove_top_directory():
    assert utils.remove_top_directory("test.cbz") == "test.cbz"
    assert utils.remove_top_directory("test_dir/test.cbr") == "test.cbr"


def test_traverse(fs):
    fs.create_dir("test_dir")
    fs.create_dir("test_dir/nested_dir")

    fs.create_file("test_dir/test_1.jpg")
    fs.create_file("test_dir/test_2.jpg")

    fs.create_file("test_dir/nested_dir/test_3.jpg")
    fs.create_file("test_dir/nested_dir/test_4.jpg")

    expected_order = [
        ("test_dir/nested_dir", "test_3.jpg"),
        ("test_dir/nested_dir", "test_4.jpg"),
        ("test_dir", "nested_dir"),
        ("test_dir", "test_1.jpg"),
        ("test_dir", "test_2.jpg")
    ]

    idx = 0

    for dirname, item in utils.traverse("test_dir"):
        assert dirname == expected_order[idx][0]
        assert item == expected_order[idx][1]
        idx += 1
