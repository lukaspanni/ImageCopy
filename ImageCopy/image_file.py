"""
Image File + copy
"""
import os
import platform
import time
from pathlib import Path


class ImageFile:
    """
    Representation of an image
    """

    raw_extensions = [".arw", ".srf", ".sr2", ".crw", ".cr2", ".cr3", ".dng", ".nef", ".nrw", ".raw", ".rw2", ".rwl",
                      ".orf", ".raf"]
    image_extensions = [".jpg", ".jpeg"]

    def __init__(self, path: Path, ext: str):
        self.path = path
        self.extension = ext

    def is_raw(self) -> bool:
        """
        Check if the file has a known RAW extension

        :return: True if extension is in list of raw_estensions
        """
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

    def get_filename(self) -> str:
        return os.path.basename(self.path)
