from ImageCopy.Transformers.PathTransform import PathTransform


class RenameTransform(PathTransform):
    """
    Regex-Rename images during copy
    """

    def _load_config(self, config: dict):
        """
        Load rename config
        """
        if "regex_in" in config:
            self.regex_in = config["regex_in"]
            if "regex_out" in config:
                self.regex_out = config["regex_out"]
            else:
                raise ValueError("Invalid rename-config, regex_out missing")
        else:
            raise ValueError("Invalid rename-config, regex_in missing")

    def transform(self, input_dict: dict):
        raise NotImplementedError()
