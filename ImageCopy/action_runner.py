"""
Action Runner
"""
from multiprocessing import Queue
from typing import Callable

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
        self.path_transformers = []
        self.after_actions = []
        if config.grouping:
            self.path_transformers.append(GroupingTransform(config.grouping))
        if config.raw_separate:
            self.path_transformers.append(RawSeparateTransform(config.raw_separate))
        if config.rename:
            self.path_transformers.append(RenameTransform(config.rename))
        if config.exif:
            self.after_actions.append(ExifEditing(config.exif))
        if config.greyscale:
            self.after_actions.append(AutoGreyscale(config.greyscale))

    def execute_transformers(self, images: dict):
        """
        Execute configured transformers for every image

        :param images: dictionary of images with output-path
        """
        for transformer in self.path_transformers:
            transformer.transform(images)

    def get_after_action_count(self):
        return len(self.after_actions)

    def execute_after_actions(self, images: dict, register_progress: Callable):
        """
        Execute configured after copy actions for every image

        :param images: dictionary of images with output-path
        :param register_progress:  function to register progress
        """
        for action in self.after_actions:
            action.execute(images)
            register_progress()

    @staticmethod
    def after_action_process(after_actions: list, image_queue: Queue, feedback_queue: Queue):
        counter = 0
        while not (command := image_queue.get()) == "END":
            if type(command) is dict:
                for action in after_actions:
                    action.execute(command)
                counter += 1
                feedback_queue.put(counter)
        feedback_queue.put("END")