import os

from zipfile import ZipFile
from unrar.rarfile import RarFile

from comics import handler, utils


supported_extensions = {
    ".zip": ZipFile,
    ".cbz": ZipFile,
    ".rar": RarFile,
    ".cbr": RarFile
}


class Archive:
    def __init__(self, path: str):
        ext = utils.get_file_extension(path)

        handler.file_not_found(path)
        handler.unsupported_extension(ext, supported_extensions)

        self.path = path
        self.dirname, self.filename = os.path.split(path)
        self.ext = ext

    @staticmethod
    def compress(source: str, target: str, exclude_dir: bool = False):
        '''Create new file archive.

        Add the contents of a directory to a new file archive. The format of
        the archive is inferred from the file extension.

        Args:
            source (str): Path to source directory.
            target (str): Path to target file archive.
            exclude_dir (bool): Exclude top level directory.
        '''

        ext = utils.get_file_extension(target)

        handler.file_not_found(source)
        handler.unsupported_extension(ext, supported_extensions)

        tool = supported_extensions[ext]

        with tool(target, mode='w') as archive:
            for dirname, item in utils.traverse(source):
                path, arcname = os.path.join(dirname, item), None

                if exclude_dir:
                    arcname = utils.remove_top_directory(path)

                archive.write(path, arcname=arcname)

    def uncompress(self, output_path: str = None):
        '''Uncompress file archive.

        Uncompress the content of the file archive. If output_path is not
        specified, will default to the same directory.

        Args:
            output_path (str): Path for uncompressed data.
        '''

        tool = supported_extensions[self.ext]

        with tool(self.path) as archive:
            archive.extractall(output_path or self.dirname)

    def search(self, query: str) -> list[str]:
        '''Search the file archive.

        Recursively searches the file archive for any item that matches
        the query.

        Args:
            query (str): Search query.

        Returns:
            A list of items within the archive that match the query.
        '''

        if not query:
            return []

        tool = supported_extensions[self.ext]

        with tool(self.path) as archive:
            return [item for item in archive.namelist() if query in item]
