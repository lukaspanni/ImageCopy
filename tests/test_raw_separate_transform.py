"""
Tests for RawSeparate
"""
import os
from pathlib import Path

from ImageCopy.Transformers.raw_separate_transform import RawSeparateTransform
from ImageCopy.image_file import ImageFile


class TestRawSeparateTransform:
    """
    Testsuite for raw separate
    """

    def test_transform(self):
        transform = RawSeparateTransform({"separate_raw": True, "raw_dir_name": "RAW"})
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg")]
        test_dict = {img: "/output/" for img in imgs}
        expected_output = [os.path.join("/output/", "RAW/"), "/output/"]
        transform.transform(test_dict)
        actual_output = list(test_dict.values())
        assert actual_output == expected_output

    def test_constructor_config_correct(self):
        raw_directory = "/test/directory/"
        config_dict = {"separate_raw": True, "raw_dir_name": raw_directory}
        raw_separate_transform = RawSeparateTransform(config_dict)
        assert raw_separate_transform.raw_dir_name == raw_directory

    def test_constructor_invalid_config_defaults(self):
        default_raw_directory = "RAW/"
        config_dict = {"separate_raw": True}
        raw_separate_transform = RawSeparateTransform(config_dict)
        assert raw_separate_transform.raw_dir_name == default_raw_directory

    def test_constructor_no_config(self):
        raw_separate_transform = RawSeparateTransform({})
        assert raw_separate_transform.raw_dir_name is None