import os
from pathlib import Path
from typing import Union


class ImageFile:
    raw_extensions = [".arw", ".srf", ".sr2", ".crw", ".cr2", ".cr3", ".dng", ".nef", ".nrw", ".raw", ".rw2", ".rwl",
                      ".orf", ".raf"]
    image_extensions = [".jpg", ".jpeg"]

    @staticmethod
    def get_images(directory: Union[str, Path], filter_extensions: list = None):
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

    def is_raw(self):
        return self.extension in ImageFile.raw_extensions

    def __str__(self):
        return str(self.path)
