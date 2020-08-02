import os
from pathlib import Path

from ImageCopy.Transformers.RawSeparateTransform import RawSeparateTransform
from ImageCopy.ImageFile import ImageFile


class TestRawSeparateTransform:
    transform = RawSeparateTransform({"separate_raw": True, "raw_dir_name": "RAW"})

    def test_transform(self):
        imgs = [ImageFile(Path("/lol/img.raw"), ".raw"), ImageFile(Path("/lol/img.jmg"), ".jpg")]
        test_dict = {img: "/output/" for img in imgs}
        expected_output = [os.path.join("/output/", "RAW/"), "/output/"]
        self.transform.transform(test_dict)
        actual_output = [v for v in test_dict.values()]
        assert actual_output == expected_output
