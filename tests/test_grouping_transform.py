"""
Tests for Grouping
"""
import time
from pathlib import Path
from random import randrange, seed
import pytest

from ImageCopy.Transformers.grouping_transform import GroupingTransform
from ImageCopy.image_file import ImageFile


def create_time():
    return time.localtime(time.mktime((randrange(2000, 2030), randrange(1, 12), randrange(1, 31), randrange(0, 24),
                                       randrange(0, 60), 0, 0, 0, 0)))


class TestGroupingTransform:
    """
    Testsuite for grouping
    """
    creation_times: list

    @pytest.fixture(autouse=True)
    def setup(self):
        seed(1337)
        self.creation_times = []

    def mock_times(self):
        cr_time = self.creation_times[0]
        self.creation_times = self.creation_times[1:]
        return cr_time

    def test_transform_year(self):
        transform = GroupingTransform({"year": "yes"})
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg"),
                ImageFile(Path("/lol/img2.jmg"), ".jpg")]
        expected_output = {img: "/output/" for img in imgs}
        for img in imgs:
            creation_time = create_time()
            self.creation_times.append(creation_time)
            img.get_creation_time = self.mock_times
            expected_output[img] = expected_output[img] + str(creation_time.tm_year) + "/"
        test_dict = {img: "/output/" for img in imgs}
        transform.transform(test_dict)
        assert list(test_dict.values()) == list(expected_output.values())

    def test_transform_year_month(self):
        transform = GroupingTransform({"year": "yes", "month": "yes"})
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg"),
                ImageFile(Path("/lol/img2.jmg"), ".jpg")]
        expected_output = {img: "/output/" for img in imgs}
        for img in imgs:
            creation_time = create_time()
            self.creation_times.append(creation_time)
            img.get_creation_time = self.mock_times
            expected_output[img] = expected_output[img] + str(creation_time.tm_year) + "/" + \
                                   str(creation_time.tm_mon) + "/"
        test_dict = {img: "/output/" for img in imgs}
        transform.transform(test_dict)
        assert list(test_dict.values()) == list(expected_output.values())

    def test_transform_year_monthname(self):
        transform = GroupingTransform({"year": "yes", "month": "yes", "month_named": "yes"})
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg"),
                ImageFile(Path("/lol/img2.jmg"), ".jpg")]
        expected_output = {img: "/output/" for img in imgs}
        for img in imgs:
            creation_time = create_time()
            self.creation_times.append(creation_time)
            img.get_creation_time = self.mock_times
            month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                           "October", "November", "December"]
            expected_output[img] = expected_output[img] + str(creation_time.tm_year) + "/" + \
                                   str(month_names[creation_time.tm_mon - 1]) + "/"
        test_dict = {img: "/output/" for img in imgs}
        transform.transform(test_dict)
        assert list(test_dict.values()) == list(expected_output.values())

    def test_transform_year_month_day(self):
        transform = GroupingTransform({"year": "yes", "month": "yes", "day": "yes"})
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg"),
                ImageFile(Path("/lol/img2.jmg"), ".jpg")]
        expected_output = {img: "/output/" for img in imgs}
        for img in imgs:
            creation_time = create_time()
            self.creation_times.append(creation_time)
            img.get_creation_time = self.mock_times
            expected_output[img] = expected_output[img] + str(creation_time.tm_year) + "/" + \
                                   str(creation_time.tm_mon) + "/" + str(creation_time.tm_mday) + "/"
        test_dict = {img: "/output/" for img in imgs}
        transform.transform(test_dict)
        assert list(test_dict.values()) == list(expected_output.values())
