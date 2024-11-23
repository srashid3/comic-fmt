# comic-fmt

A command line tool for managing CBR/CBZ files.

## Installation

Clone this repo and install with `pip`.

```
$ pip install .
```

Note that comic-fmt depends on the `unrar` utility. Set `UNRAR_LIB_PATH` to the location of the library.

## Usage

```
Usage: comic-fmt [OPTIONS] COMMAND [ARGS]...

  Manage file archives for comic books.

  If the PATH for a command is a directory, then the operation is
  automatically applied to all file archives within the directory.

Options:
  --help  Show this message and exit.

Commands:
  cbz         Convert to CBZ format.
  pages       Format page names.
  rename      Rename file archive.
  search      Search file archive.
  uncompress  Uncompress file archive.
```

## Development

The underlying module used by comic-fmt is available for scripting and automation.

```python
from comics import Comic

c = Comic("test.cbr")

c.covert()
c.rename(cleanup=True)
```

The file archive can be modified with edit mode. Any changes will not be persisted until the comic is saved.

```python
c = Comic("test.cbz")

c.edit()
c.flatten()
c.format_pages(page_name="Page ", page_regex=r"\d+")
c.save()
```

When used as a context manager, the comic is implicitly saved upon exit.

```python
with Comic("test.cbz") as c:
    c.flatten()
    c.format_pages(page_name="Page ", page_regex=r"\d+")
```

The contents of the file archive can be accessed with the temporary directory.

```python
with Comic("test.cbz") as c:
    for item is os.listdir(c.temp_dir):
        custom_logic(item)
```

Refer to the documentation in `comic.py` for more information on the available methods.
