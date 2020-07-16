import os

from ImageCopy.PathTransform import PathTransform
from ImageCopy.image_file import ImageFile
from enum import Enum


class GroupBy(Enum):
    """
    Possible groups.
    """
    YEAR = 1
    MONTH = 2
    MONTH_NAMED = 3
    DAY = 4


class GroupingTransform(PathTransform):
    """
    Used to group images by creation time.
    """

    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"]

    def __init__(self, grouping_config: set):
        super().__init__()
        self.grouping_config = grouping_config

    def transform(self, input_dict: dict):
        if len(self.grouping_config) < 1:
            return
        for image in input_dict:
            group = self._get_group_directory(image)
            input_dict[image] = os.path.join(input_dict[image], group)

    def _get_group_directory(self, image: ImageFile) -> str:
        """
        Get the group directory name (based on creation time and configured groups) of a given image.
        :param image: image file
        :return: name of the group directory
        """
        group_directory = ""
        creation_time = image.get_creation_time()
        if GroupBy.YEAR in self.grouping_config:
            group_directory += str(creation_time.tm_year) + "/"
        if GroupBy.MONTH_NAMED in self.grouping_config:
            group_directory += self.month_names[creation_time.tm_mon - 1] + "/"
        else:  # only group month once
            if GroupBy.MONTH in self.grouping_config:
                group_directory += str(creation_time.tm_mon) + "/"
        if GroupBy.DAY in self.grouping_config:
            group_directory += str(creation_time.tm_mday) + "/"
        return group_directory


def test(input_dict):
    for e in input_dict:
        input_dict[e] += str(e)


if __name__ == "__main__":
    test_dict = {1: "Lol", 2: "LEL"}
    print(test_dict)
    test(test_dict)
    print(test_dict)