"""
Tests for Rename
"""

import pytest
from ImageCopy.Transformers.rename_transform import RenameTransform
from ImageCopy.image_file import ImageFile
from pathlib import Path


class TestRenameTransform:
    """
    Testsuite for rename
    """

    def test_constructor_config_correct(self):
        config_dict = {"in": "ExampleString", "out": "ExampleOutputString"}
        rename_transform = RenameTransform(config_dict)
        assert rename_transform.in_str == config_dict["in"]
        assert rename_transform.out_str == config_dict["out"]

    def test_constructor_parts_missing(self):
        config_dict = {"out": "ExampleOutputString"}
        with pytest.raises(ValueError):
            rename_transform = RenameTransform(config_dict)
        config_dict = {"in": "ExampleString"}
        with pytest.raises(ValueError):
            rename_transform = RenameTransform(config_dict)

    def test_constructor_invalid_types(self):
        config_dict = {"in": 42, "out": True}
        with pytest.raises(ValueError):
            rename_transform = RenameTransform(config_dict)

    def test_transform(self):
        config_dict = {"in": "DSC_", "out": "IMAGE-"}
        rename_transform = RenameTransform(config_dict)
        input_dict = {
            ImageFile(Path("input_path/DSC_00001.JPG"), ".JPG"): "output_path/",
            ImageFile(Path("input_path/DSC_00002.JPG"), ".JPG"): "output_path/",
            ImageFile(Path("input_path/DSC_12042.JPG"), ".JPG"): "output_path/",
            ImageFile(Path("input_path/DSC_137_DSC.JPG"), ".JPG"): "output_path/",
        }
        key_list = list(input_dict.keys())
        expected_out = {
            key_list[0]: "output_path/IMAGE-00001.JPG",
            key_list[1]: "output_path/IMAGE-00002.JPG",
            key_list[2]: "output_path/IMAGE-12042.JPG",
            key_list[3]: "output_path/IMAGE-137_DSC.JPG"
        }
        rename_transform.transform(input_dict)
        assert input_dict == expected_out
