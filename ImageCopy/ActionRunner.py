from ImageCopy.Actions.AutoGreyscale import AutoGreyscale
from ImageCopy.Actions.ExifEditing import ExifEditing
from ImageCopy.Transformers.GroupingTransform import GroupingTransform
from ImageCopy.Transformers.RawSeparateTransform import RawSeparateTransform
from ImageCopy.Config import Config


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
        if self.config.exif is not None:
            self.after_actions.append(ExifEditing(self.config.exif))
        if self.config.greyscale is not None:
            self.after_actions.append(AutoGreyscale(self.config.greyscale))

    def execute_transform(self, images: dict):
        for transformer in self.path_transformers:
            transformer.transform(images)

    def execute_after_actions(self, images: dict):
        for action in self.after_actions:
            action.execute(images)
