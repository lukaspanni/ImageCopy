from GroupingTransform import GroupingTransform
from RawSeparateTransform import RawSeparateTransform
from config import Config


class TransformRunner:

    def __init__(self, config: Config):
        self.config = config
        self.transformers = []
        if self.config.group is not None:
            self.transformers.append(GroupingTransform(self.config.group))
        if self.config.io.separate_raw:
            self.transformers.append(RawSeparateTransform(config.io.raw_dir_name))

    def execute_transform(self, images: dict):
        for transformer in self.transformers:
            transformer.transform(images)