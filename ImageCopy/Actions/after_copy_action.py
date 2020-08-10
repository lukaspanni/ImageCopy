"""
After copy action abstract base class
"""
from abc import ABC, abstractmethod


class AfterCopyAction(ABC):
    """
    Execute actions after copying images
    """

    @abstractmethod
    def execute(self, images: dict):
        """
        Execute an after copy action
        :param images: dictionary of ImageFile-objects and target paths
        """
