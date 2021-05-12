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
        if "in" in config and isinstance(config["in"], str):
            self.in_str = config["in"]
        else:
            raise ValueError("Invalid rename-config, regex_in missing")

        if "out" in config and isinstance(config["out"], str):
            self.out_str = config["out"]
        else:
            raise ValueError("Invalid rename-config, regex_out missing")

    def transform(self, input_dict: dict):
        """
        Replace in the file name using a regular expression
        """
        regex = re.compile(self.in_str, re.IGNORECASE)
        for file in input_dict:
            renamed = regex.sub(self.out_str, file.path.name)
            input_dict[file] = os.path.join(input_dict[file], renamed)
