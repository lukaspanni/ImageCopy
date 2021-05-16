from ImageCopy.Actions.after_copy_action import AfterCopyAction
from ImageCopy.Transformers.path_transform import PathTransform
from ImageCopy.config import Config

"""
Collection of Mock-Implementations
Refactor in multiple files if more than 4 Mock-Classes or one Mock-Class with more than 4 Methods or code lines > 50
"""


class MockConfig(Config):
    def __init__(self, grouping=None, raw_separate=None, rename=None, exif=None):
        self.grouping = grouping
        self.raw_separate = raw_separate
        self.rename = rename
        self.exif = exif


class MockTransformer(PathTransform):

    def __init__(self):
        self.transform_called = False
        self.transform_called_with = dict()

    def transform(self, input_dict: dict):
        self.transform_called = True
        self.transform_called_with = input_dict

    def _load_config(self, config):
        pass


class MockAction(AfterCopyAction):

    def __init__(self):
        self.execute_called = False
        self.execute_called_with = dict()

    def execute(self, images: dict):
        self.execute_called = True
        self.execute_called_with = images
