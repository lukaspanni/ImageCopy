"""
Auto greyscale
"""
import os
import numpy as np
from PIL import Image
from ImageCopy.Actions.after_copy_action import AfterCopyAction
from ImageCopy.Actions.greyscale_converter import GreyscaleConverter


class AutoGreyscale(AfterCopyAction):
    """
    Creates a greyscale copy of copied images
    """

    def __init__(self, config: dict):
        self.converter = GreyscaleConverter()
        if 'algorithm' not in config:
            self.converter.algorithm = "average"
        else:
            self.converter.algorithm = config['algorithm']
        if 'file_name' not in config:
            self.file_name = "greyscale"
        else:
            self.file_name = config['file_name']

    def execute(self, images: dict):
        for img in images:
            if not img.is_raw():
                pil_img = Image.open(images[img])
                img_data = np.array(pil_img)
                pil_img = None
                greyscale_img = Image.fromarray(self.converter.execute(img_data))
                path = os.path.splitext(images[img])
                greyscale_img.save(path[0] + "_" + self.file_name + path[1])
                img_data = None
                greyscale_img = None
