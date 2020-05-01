import os
import shutil

from image_file import ImageFile


class ImageCopier:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def copy(self, image: ImageFile):
        shutil.copy2(str(image), self.output_dir)


class RAWSeparateImageCopier(ImageCopier):
    def __init__(self, output_dir, raw_dir_name):
        super().__init__(output_dir)
        self.raw_dir = output_dir + raw_dir_name
        if not os.path.exists(self.raw_dir):
            os.mkdir(self.raw_dir)

    def copy(self, image: ImageFile):
        if image.is_raw():
            shutil.copy2(str(image), self.raw_dir)
        else:
            shutil.copy2(str(image), self.output_dir)
