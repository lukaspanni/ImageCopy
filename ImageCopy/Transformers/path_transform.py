"""
Base for PathTransformers
"""
from abc import ABC, abstractmethod


class PathTransform(ABC):
    """
    Base class for other transformers
    """

    def __init__(self, config: dict):
        self._load_config(config)

    @abstractmethod
    def transform(self, input_dict: dict):
        """
        Execute transformation on images

        :param input_dict: dictionary of images with output-path
        """
        pass

    @abstractmethod
    def _load_config(self, config):
        """
        Load config for current transformer

        :param config: configuration dictionary for current transformer
        """
        pass
