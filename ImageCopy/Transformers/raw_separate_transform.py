"""
Raw Separate Feature
"""
import os

from ImageCopy.Transformers.path_transform import PathTransform


class RawSeparateTransform(PathTransform):
    """
    Separate Raw files in different folder
    """

    def _load_config(self, config):
        if 'separate_raw' in config and config['separate_raw']:
            if 'raw_dir_name' in config:
                self.raw_dir_name = config['raw_dir_name']
                if self.raw_dir_name[-1] != "/":
                    self.raw_dir_name += "/"
            else:
                self.raw_dir_name = "RAW/"
            return
        self.raw_dir_name = None

    def transform(self, input_dict: dict):
        if self.raw_dir_name is None:
            return
        for image in input_dict:
            if image.is_raw():
                input_dict[image] = os.path.join(input_dict[image], self.raw_dir_name)
