from typing import Optional

import piexif

from AfterCopyAction import AfterCopyAction


class ExifEditing(AfterCopyAction):

    def __init__(self, exif_data: dict):
        self.exif_data = exif_data

    def set_exif_data(self, image: str):
        """
        Sets exif data in Image.
        Currently only for JPGs.
        :param image: Path to image
        """
        exif = piexif.load(image)
        for key in self.exif_data:
            exif['0th'][key] = self.exif_data[key]
        exif_bytes = piexif.dump(exif)
        piexif.insert(exif_bytes, image)

    def execute(self, output_paths: list):
        for path in output_paths:
            self.set_exif_data(path)
