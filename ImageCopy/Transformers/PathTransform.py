from abc import ABC, abstractmethod


class PathTransform(ABC):
    """
    Transform ImageFile-Dictionary output path
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def transform(self, input_dict: dict):
        pass
