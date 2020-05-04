from image_file import ImageFile
from enum import Enum
from time import localtime


class GroupBy(Enum):
    """
    Possible groups.
    """
    YEAR = 1
    MONTH = 2
    MONTH_NAMED = 3
    DAY = 4


class Grouper:
    """
    Used to group images by creation time.
    """
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                   "November", "December"]

    def __init__(self, group_list: set):
        self.group_list = group_list

    def get_group_directory(self, image: ImageFile) -> str:
        """
        Get the group directory name (based on creation time and configured groups) of a given image.
        :param image: image file
        :return: name of the group directory
        """
        if len(self.group_list) < 1:
            return ""
        group_directory = ""
        creation_time = image.get_creation_time()
        if GroupBy.YEAR in self.group_list:
            group_directory += str(creation_time.tm_year) + "/"
        if GroupBy.MONTH_NAMED in self.group_list:
            group_directory += Grouper.month_names[creation_time.tm_mon - 1] + "/"
        else:   # only group month once
            if GroupBy.MONTH in self.group_list:
                group_directory += str(creation_time.tm_mon) + "/"
        if GroupBy.DAY in self.group_list:
            group_directory += str(creation_time.tm_mday) + "/"
        return group_directory
