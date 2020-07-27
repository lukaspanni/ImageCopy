import os

import yaml


class Config:
    class _in_outConfig:
        input_dir: str
        output_dir: str

        def __init__(self, io_config: dict):
            """
            Load input-output configuration.
            :param io_config:
            """
            if 'input_dir' in io_config and os.path.exists(io_config['input_dir']):
                self.input_dir = io_config['input_dir']
            if 'output_dir' in io_config:
                self.output_dir = io_config['output_dir']

    def __init__(self, config_path):
        """
        Crate Config-Object and load configuration from config_path.
        :param config_path: path to yaml config-file
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError("Config file" + config_path + "not found.")

        with open(config_path, "r") as yml:
            self._cfg = yaml.load(yml, Loader=yaml.SafeLoader)

        self.io = None
        self.config_modules = []
        self._load_config()

    def _load_config(self):
        """

        """
        if self._cfg is not None:
            if "modules" in self._cfg:
                for module in self._cfg["modules"]:
                    self.config_modules.append(module)
                    if module not in self._cfg:
                        raise ValueError("No " + module + " config found")

            if 'input_output' in self._cfg:
                self.io = self._in_outConfig(self._cfg['input_output'])
            else:
                raise ValueError("No input output config found")

    def __getattr__(self, item):
        if item in self._cfg:
            return self._cfg[item]
