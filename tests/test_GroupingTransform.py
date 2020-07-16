import copy
import time
from pathlib import Path
from random import randrange, seed

from ImageCopy.GroupingTransform import GroupingTransform, GroupBy
from ImageCopy.image_file import ImageFile


class TestGroupingTransform:
    transform = GroupingTransform({GroupBy.YEAR, GroupBy.MONTH})
    seed(1337)
    creation_times = []

    def create_time(self):
        return time.localtime(time.mktime((randrange(2000, 2030), randrange(1, 12), randrange(1, 31), randrange(0, 24),
                                           randrange(0, 60), 0, 0, 0, 0)))

    def mock_times(self):
        time = self.creation_times[0]
        self.creation_times = self.creation_times[1:]
        return time

    def test_transform(self):
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg"),
                ImageFile(Path("/lol/img2.jmg"), ".jpg")]
        expected_output = {img: "/output/" for img in imgs}
        for img in imgs:
            creation_time = self.create_time()
            self.creation_times.append(creation_time)
            img.get_creation_time = self.mock_times
            expected_output[img] = expected_output[
                                       img] + str(creation_time.tm_year) + "/" + str(creation_time.tm_mon) + "/"
        test_dict = {img: "/output/" for img in imgs}
        self.transform.transform(test_dict)
        assert list(test_dict.values()) == list(expected_output.values())
