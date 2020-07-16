import os

from ExifEditing import ExifEditing
from GroupingTransform import GroupingTransform
from RawSeparateTransform import RawSeparateTransform
from config import Config


class ActionRunner:
    """
    Run path transforms (pre copy) and after copy actions
    """

    def __init__(self, config: Config):
        self.config = config
        self.path_transformers = []
        self.after_actions = []
        if self.config.group is not None:
            self.path_transformers.append(GroupingTransform(self.config.group))
        if self.config.io.separate_raw:
            self.path_transformers.append(RawSeparateTransform(config.io.raw_dir_name))
        if self.config.exif is not None:
            self.after_actions.append(ExifEditing(self.config.exif))

    def execute_transform(self, images: dict):
        for transformer in self.path_transformers:
            transformer.transform(images)

    def execute_after_actions(self, images: dict):
        image_paths = [path for path in images.values()]
        for action in self.after_actions:
            action.execute(image_paths)
