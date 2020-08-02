import os

from ImageCopy.Transformers.PathTransform import PathTransform


class RawSeparateTransform(PathTransform):

    def __init__(self, config: dict):
        super().__init__(config)

    def _load_config(self, config):
        if 'separate_raw' in config and config['separate_raw']:
            if 'raw_dir_name' in config:
                self.raw_dir_name = config['raw_dir_name']
                if self.raw_dir_name[-1] != "/":
                    self.raw_dir_name += "/"
            else:
                self.raw_dir_name = "RAW/"

    def transform(self, input_dict: dict):
        if self.raw_dir_name is None:
            return
        for image in input_dict:
            if image.is_raw():
                input_dict[image] = os.path.join(input_dict[image], self.raw_dir_name)
