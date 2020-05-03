import os
import shutil
from typing import Optional

from grouper import Grouper
from image_file import ImageFile


class ImageCopier:
    def __init__(self, output_dir: str, grouping: Optional[Grouper] = None):
        self.output_dir = output_dir
        self.grouping = grouping
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def get_destination_directory(self, image):
        destination = self.output_dir
        if self.grouping is not None:
            destination += self.grouping.get_group_directory(image)
        return destination

    def copy(self, image: ImageFile):
        destination_dir = self.get_destination_directory(image)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)
        shutil.copy2(str(image), destination_dir)


class RAWSeparateImageCopier(ImageCopier):
    def __init__(self, output_dir: str, raw_dir_name: str, grouping: Optional[Grouper] = None):
        super().__init__(output_dir, grouping)
        self.raw_dir_name = raw_dir_name

    def copy(self, image: ImageFile):
        destination_dir = self.get_destination_directory(image)
        if image.is_raw():
            destination_dir = destination_dir + self.raw_dir_name
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)
        shutil.copy2(str(image), destination_dir)