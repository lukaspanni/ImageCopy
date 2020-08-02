import os

from ImageCopy.Transformers.PathTransform import PathTransform
from ImageCopy.ImageFile import ImageFile
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

    def _load_config(self, config):
        """
        Load grouping config into set of group-actions.
        """
        self.grouping_config = set()
        if 'year' in config and config['year']:
            self.grouping_config.add(GroupBy.YEAR)
        if 'month' in config and config['month']:
            if 'month_named' in config and config['month_named']:
                self.grouping_config.add(GroupBy.MONTH_NAMED)
            else:
                self.grouping_config.add(GroupBy.MONTH)
        if 'day' in config and config['day']:
            self.grouping_config.add(GroupBy.DAY)

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
