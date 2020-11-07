"""
After copy action abstract base class
"""
from abc import ABC, abstractmethod


class AfterCopyAction(ABC):
    """
    Base class for executing actions after copying
    """

    @abstractmethod
    def execute(self, images: dict):
        """
        Execute an after copy action

        :param images: dictionary of images with output-path
        """
