import os
import shutil
from ImageCopy.image_file import ImageFile


def copy(image: ImageFile, destination: str):
    """
    Copy the image to its new location.
    :param image: image file to copy.
    :param destination: destination directory
    """
    # self.set_exif_data(image)
    if not os.path.exists(destination):
        os.makedirs(destination, exist_ok=True)
    return shutil.copy2(str(image), destination)
