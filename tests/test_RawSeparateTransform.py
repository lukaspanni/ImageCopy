import os
from pathlib import Path

from ImageCopy.RawSeparateTransform import RawSeparateTransform
from ImageCopy.image_file import ImageFile


class TestRawSeparateTransform:
    transform = RawSeparateTransform("RAW")

    def test_transform(self):
        test_dict = {ImageFile(Path("/lol/img.raw"), ".raw"): "/output/",
                     ImageFile(Path("/lol/img.jmg"), ".jpg"): "/output/"}
        expected_output = [os.path.join("/output/", "RAW"), "/output/"]
        self.transform.transform(test_dict)
        actual_output = [v for v in test_dict.values()]
        assert expected_output == actual_output
