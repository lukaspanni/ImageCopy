from abc import ABC, abstractmethod


class AfterCopyAction(ABC):
    """
    Execute actions after copying images
    """

    @abstractmethod
    def execute(self, output_paths: list):
        pass
