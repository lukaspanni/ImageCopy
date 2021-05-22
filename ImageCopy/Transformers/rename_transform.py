"""
Rename Feature
"""
import os
import re

from ImageCopy.Transformers.path_transform import PathTransform


class RenameTransform(PathTransform):
    """
    Rename images during copy by replacing parts of the old name
    """

    def _load_config(self, config: dict):
        """
        Load rename config
        """
        if "in" not in config or "out" not in config:
            raise ValueError("Invalid rename-config, regex_in/regex_out missing")
        if not isinstance(config["in"], str) or not isinstance(config["out"], str):
            raise ValueError("Invalid rename-config, regex_in/regex_out has wrong type")

        self.in_str = config["in"]
        self.out_str = config["out"]

    def transform(self, input_dict: dict):
        """
        Replace in the file name using a regular expression
        """
        regex = re.compile(self.in_str, re.IGNORECASE)
        for file in input_dict:
            renamed = regex.sub(self.out_str, file.path.name)
            input_dict[file] = os.path.join(input_dict[file], renamed)
