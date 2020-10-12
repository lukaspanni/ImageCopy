"""
Action Runner
"""
from ImageCopy.Actions.auto_greyscale import AutoGreyscale
from ImageCopy.Actions.exif_editing import ExifEditing
from ImageCopy.Transformers.grouping_transform import GroupingTransform
from ImageCopy.Transformers.raw_separate_transform import RawSeparateTransform
from ImageCopy.config import Config
from ImageCopy.Transformers.rename_transform import RenameTransform


class ActionRunner:
    """
    Run path transforms (pre copy) and after copy actions
    """

    def __init__(self, config: Config):
        self.config = config
        self.path_transformers = []
        self.after_actions = []
        if self.config.grouping is not None:
            self.path_transformers.append(GroupingTransform(self.config.grouping))
        if self.config.raw_separate:
            self.path_transformers.append(RawSeparateTransform(config.raw_separate))
        if self.config.rename:
            self.path_transformers.append(RenameTransform(config.rename))
        if self.config.exif is not None:
            self.after_actions.append(ExifEditing(self.config.exif))
        if self.config.greyscale is not None:
            self.after_actions.append(AutoGreyscale(self.config.greyscale))

    def execute_transformers(self, images: dict):
        """
        Execute configured transformers for every image

        :param images: dictionary of images with output-path
        """
        for transformer in self.path_transformers:
            transformer.transform(images)

    def execute_after_actions(self, images: dict):
        """
        Execute configured after copy actions for every image

        :param images: dictionary of images with output-path
        """
        for action in self.after_actions:
            action.execute(images)
