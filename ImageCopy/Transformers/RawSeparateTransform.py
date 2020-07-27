import os

from ImageCopy.Transformers.PathTransform import PathTransform


def _load_raw_separate_config(config: dict):
    if 'separate_raw' in config and config['separate_raw']:
        if 'raw_dir_name' in config:
            return config['raw_dir_name']
        else:
            return "RAW"
    return None


class RawSeparateTransform(PathTransform):
    def __init__(self, config: dict):
        super().__init__()
        self.raw_dir_name = _load_raw_separate_config(config)

    def transform(self, input_dict: dict):
        if self.raw_dir_name is None:
            return
        for image in input_dict:
            if image.is_raw():
                input_dict[image] = os.path.join(input_dict[image], self.raw_dir_name)
