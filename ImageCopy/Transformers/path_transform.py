"""
Base for PathTransformers
"""
from abc import ABC, abstractmethod


class PathTransform(ABC):
    """
    Transform ImageFile-Dictionary output path
    """

    def __init__(self, config: dict):
        self._load_config(config)

    @abstractmethod
    def transform(self, input_dict: dict):
        pass

    @abstractmethod
    def _load_config(self, config):
        pass
