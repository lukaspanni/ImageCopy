import os

import piexif
import yaml

from GroupingTransform import GroupBy


class Config:
    class _in_outConfig:
        input_dir: str
        output_dir: str
        separate_raw: bool
        raw_dir_name: str

        def __init__(self, io_config: dict):
            """
            Load input-output configuration.
            :param io_config:
            """
            if 'input_dir' in io_config and os.path.exists(io_config['input_dir']):
                self.input_dir = io_config['input_dir']
            if 'output_dir' in io_config:
                self.output_dir = io_config['output_dir']
            if 'separate_raw' in io_config:
                self.separate_raw = io_config['separate_raw']
            if 'raw_dir_name' in io_config:
                self.raw_dir_name = io_config['raw_dir_name']

    def __init__(self, config_path):
        """
        Crate Config-Object and load configuration from config_path.
        :param config_path: path to yaml config-file
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError("Config file" + config_path + "not found.")

        with open(config_path, "r") as yml:
            self.cfg = yaml.load(yml, Loader=yaml.SafeLoader)

        self.io = None
        self.group = None
        self.exif = None
        self._load_config()

    def _load_config(self):
        """
        Load config values into object.
        """
        if self.cfg is not None:
            if 'input-output' in self.cfg:
                self.io = self._in_outConfig(self.cfg['input-output'])
            else:
                raise ValueError("No input-output config")
            self._load_grouping_config()
            self._load_exif_config()

    def _load_grouping_config(self):
        """
        Create Grouper based on grouping-config.
        """
        if 'grouping' in self.cfg:
            group_by = set()
            if 'year' in self.cfg['grouping'] and self.cfg['grouping']['year']:
                group_by.add(GroupBy.YEAR)
            if 'month' in self.cfg['grouping'] and self.cfg['grouping']['month']:
                if 'named_named' in self.cfg['grouping'] and self.cfg['grouping']['months_named']:
                    group_by.add(GroupBy.MONTH_NAMED)
                else:
                    group_by.add(GroupBy.MONTH)
            if 'day' in self.cfg['grouping'] and self.cfg['grouping']['day']:
                group_by.add(GroupBy.DAY)
            self.group = group_by

    def _load_exif_config(self):
        """
        Load exif-config and create dict of exif-tags
        """
        if 'exif' in self.cfg:
            self.exif = dict()
            if 'artist' in self.cfg['exif']:
                self.exif[piexif.ImageIFD.Artist] = self.cfg['exif']['artist']
            if 'copyright' in self.cfg['exif']:
                self.exif[piexif.ImageIFD.Copyright] = self.cfg['exif']['copyright']