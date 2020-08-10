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
    transform = RawSeparateTransform({"separate_raw": True, "raw_dir_name": "RAW"})

    def test_transform(self):
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg")]
        test_dict = {img: "/output/" for img in imgs}
        expected_output = [os.path.join("/output/", "RAW/"), "/output/"]
        self.transform.transform(test_dict)
        actual_output = list(test_dict.values())
        assert actual_output == expected_output
