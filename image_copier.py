import os
import shutil
from typing import Optional
from image_file import ImageFile


def copy(image: ImageFile, destination: str):
    """
    Copy the image to its new location.
    :param image: image file to copy.
    :param destination: destination file
    """
    # self.set_exif_data(image)
    if not os.path.exists(destination):
        os.makedirs(destination, exist_ok=True)
    shutil.copy2(str(image), destination)


    #def __init__(self, exif_data: Optional[dict] = None):
    #    self.exif_data = exif_data

    #def set_exif_data(self, image: ImageFile):
    #    """
    #    Sets exif data in Image.
    #    Currently only for JPGs.
    #    :param image: ImageFile
    #    """
    #    if self.exif_data is not None:
    #        file_path = str(image)
    #        exif = piexif.load(file_path)
    #        for key in self.exif_data:
    #            exif['0th'][key] = self.exif_data[key]
    #        exif_bytes = piexif.dump(exif)
    #        piexif.insert(exif_bytes, file_path)
