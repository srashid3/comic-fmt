import os
import re
import shutil

from comics import Archive
from comics import utils


class Comic:
    def __init__(self, path: str):
        self.__edit_mode = False

        self.archive = Archive(path)
        self.title = utils.remove_file_extension(self.archive.filename)
        self.temp_dir = "_temp"

    def __enter__(self):
        self.edit()
        return self

    def __exit__(self, exc_type, ext_val, exc_trace):
        self.save()

    def edit(self):
        '''Edit comic.

        Uncompress the comic to a temporary directory. Updates are not
        persisted until the comic is saved.
        '''

        self.__edit_mode = True
        self.uncompress(self.temp_dir)

    def save(self):
        '''Save comic.

        Compress the data in the temporary directory and overwrite the
        existing comic.

        Note that this process will convert the comic to CBZ.
        '''

        if not self.__edit_mode:
            return

        os.remove(self.archive.path)

        new_path = utils.change_file_extension(self.archive.path, ".cbz")
        Archive.compress(self.temp_dir, new_path, exclude_dir=True)

        shutil.rmtree(self.temp_dir)

        self.archive = Archive(new_path)
        self.__edit_mode = False

    def rename(self, title: str = None, cleanup: bool = False):
        '''Rename comic.

        Update the title of the comic. If cleanup is True, extra characters
        such as parentheses and brackets are removed.

        Args:
            title (str): New comic title.
            cleanup (bool): Remove extra characters from title.
        '''

        new_title = title or self.title

        if cleanup:
            new_title = re.sub(r'\(.*?\)|\[.*?\]', "", new_title)
            new_title = new_title.strip()

        if new_title == self.title:
            return

        new_filename = f'{new_title}{self.archive.ext}'
        new_path = os.path.join(self.archive.dirname, new_filename)

        os.rename(self.archive.path, new_path)

        self.title = new_title
        self.archive = Archive(new_path)

    def search(self, query: str) -> list[str]:
        '''Search comic.

        A wrapper method that searches the underlying file archive.

        Args:
            query (str): Search query.

        Returns:
            A list of items with the archive that match the query.
        '''

        return self.archive.search(query)

    def uncompress(self, output_path: str = None):
        '''Uncompress comic.

        A wrapper method that uncompresses the underlying file archive.

        Args:
            output_path (str): Path to uncompressed data.
        '''

        self.archive.uncompress(output_path=output_path)

    def convert(self):
        '''Convert to CBZ.

        Uncompress the contents of the comic and recompress as CBZ.

        If the extension is already CBZ or the comic is in edit mode,
        no action is required.
        '''

        if self.archive.ext == ".cbz" or self.__edit_mode:
            return

        self.edit()
        self.save()

    def flatten(self):
        '''Flatten directories within comic.

        Recursively moves the contents of all subdirectories to the root
        directory within the file archive.

        Note that this method requires the comic to be in edit mode.
        '''

        if not self.__edit_mode:
            self.edit()

        for dirname, item in utils.traverse(self.temp_dir):
            path = os.path.join(dirname, item)

            if os.path.isfile(path) and dirname != self.temp_dir:
                shutil.move(path, self.temp_dir)

            if os.path.isdir(path):
                shutil.rmtree(path)

    def format_pages(
        self,
        page_name: str,
        page_regex: str,
        remove: bool = False
    ):
        '''Format pages.

        Format the pages of the comic using a standard naming convention.
        Numbers are automatically padded based on the total page count.

        --------------------------------
        page_name = "Page "
        include = ".+"

        foobar_1.jpg > Page 01.jpg
        foobar_2.jpg > Page 02.jpg
        foobar_3.jpg > Page 03.jpg
        --------------------------------

        Note that this method requires the comic to be in edit mode.

        Args:
            page_name (str): Name of page.
            regex (str): Regular expression for finding pages.
            remove (bool): Remove all other files.
        '''

        if not self.__edit_mode:
            self.edit()

        page_cnt = 1

        for dirname, item in utils.traverse(self.temp_dir):
            path = os.path.join(dirname, item)

            if os.path.isdir(path):
                page_cnt = 1
                continue

            if not re.search(page_regex, item):
                if remove:
                    os.remove(path)
                continue

            num_pages = len(os.listdir(dirname))
            padding = utils.zero_padded(num_pages)
            ext = utils.get_file_extension(path)

            filename = f'{page_name}{page_cnt:{padding}}{ext}'
            new_path = os.path.join(dirname, filename)

            os.rename(path, new_path)

            page_cnt += 1
