import os
import platform
import time
from pathlib import Path
from typing import Union


class ImageFile:
    raw_extensions = [".arw", ".srf", ".sr2", ".crw", ".cr2", ".cr3", ".dng", ".nef", ".nrw", ".raw", ".rw2", ".rwl",
                      ".orf", ".raf"]
    image_extensions = [".jpg", ".jpeg"]

    @staticmethod
    def get_images(directory: Union[str, Path], filter_extensions: list = None) -> list:
        files = []
        if filter_extensions is None:
            filter_extensions = ImageFile.raw_extensions + ImageFile.image_extensions
        for entry in Path(directory).iterdir():
            if entry.is_file():
                if filter_extensions is not None:
                    name, ext = os.path.splitext(str(entry))
                    ext = ext.lower()
                    if ext in filter_extensions:
                        files.append(ImageFile(entry, ext))
                else:
                    files.append(entry)
            else:
                files += ImageFile.get_images(entry, filter_extensions)
        return files

    def __init__(self, path: Path, ext: str):
        self.path = path
        self.extension = ext

    def is_raw(self) -> bool:
        return self.extension in ImageFile.raw_extensions

    def get_creation_time(self) -> time.struct_time:
        """
        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        if platform.system() == 'Windows':
            creation_time = os.path.getctime(str(self))
        else:
            stat = os.stat(str(self))
            try:
                creation_time = stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                creation_time = stat.st_mtime
        return time.localtime(creation_time)

    def __str__(self) -> str:
        return str(self.path)
