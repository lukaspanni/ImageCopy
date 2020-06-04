import os
import shutil
from typing import Optional

import piexif

from grouper import Grouper
from image_file import ImageFile

# TODO: Clean Solution for adding functionality like Grouping, EXIF-Changes, Renaming ...

class ImageCopier:
    """
    Used to copy images  from one location to another.
    """

    def __init__(self, output_dir: str, grouping: Optional[Grouper] = None, exif_data: Optional[dict] = None):
        self.output_dir = output_dir
        self.grouping = grouping
        self.exif_data = exif_data
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def get_destination_directory(self, image) -> str:
        """
        Get the destination directory for a given image.
        The destination already includes grouping.
        :param image: image file
        :return: destination directory
        """
        destination = self.output_dir
        if self.grouping is not None:
            destination = os.path.join(destination, self.grouping.get_group_directory(image))
        return destination

    def set_exif_data(self, image: ImageFile):
        """
        Sets exif data in Image.
        Currently only for JPGs.
        :param image: ImageFile
        """
        if self.exif_data is not None:
            file_path = str(image)
            exif = piexif.load(file_path)
            for key in self.exif_data:
                exif['0th'][key] = self.exif_data[key]
            exif_bytes = piexif.dump(exif)
            piexif.insert(exif_bytes, file_path)

    def copy(self, image: ImageFile):
        """
        Copy the image to its new location.
        :param image: image file to copy.
        """
        self.set_exif_data(image)
        destination_dir = self.get_destination_directory(image)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)
        shutil.copy2(str(image), destination_dir)


class RAWSeparateImageCopier(ImageCopier):
    """
    Used to copy images and separate RAW and JPG images during copy.
    """

    def __init__(self, output_dir: str, raw_dir_name: str, grouping: Optional[Grouper] = None, exif_data: Optional[dict] = None):
        super().__init__(output_dir, grouping, exif_data)
        self.raw_dir_name = raw_dir_name

    def copy(self, image: ImageFile):
        destination_dir = self.get_destination_directory(image)
        if image.is_raw():
            destination_dir = os.path.join(destination_dir, self.raw_dir_name)
        else:
            self.set_exif_data(image)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)
        shutil.copy2(str(image), destination_dir)
