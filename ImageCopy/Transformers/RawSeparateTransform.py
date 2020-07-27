import os

from ImageCopy.Transformers.PathTransform import PathTransform


class RawSeparateTransform(PathTransform):
    def __init__(self, raw_dir_name: str):
        super().__init__()
        self.raw_dir_name = raw_dir_name

    def transform(self, input_dict: dict):
        for image in input_dict:
            if image.is_raw():
                input_dict[image] = os.path.join(input_dict[image], self.raw_dir_name)
