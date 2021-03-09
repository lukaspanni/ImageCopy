import os
import shutil
from enum import Enum

from ImageCopy.config import Config
from ImageCopy.image_file import ImageFile


class Copier:
    class OverwriteOptions(Enum):
        OVERWRITE = "always-overwrite"
        WARN = "warn-before-overwrite"
        NO_OVERWRITE = "never-overwrite"
        APPEND_SUFFIX = "append-suffix"

    def __init__(self, config: Config):
        self.mode = Copier.OverwriteOptions.OVERWRITE
        if config.copy is not None:
            if mode := config.copy["mode"] is not None:
                try:
                    self.mode = Copier.OverwriteOptions(mode)
                except ValueError:
                    pass


def copy(self, image: ImageFile, destination: str):
    """
    Copy the given image to its new location.

    :param image: image file to copy.
    :param destination: destination directory with or without new filename
    """
    split_path = destination.split("/")
    # Workaround to allow rename
    if "." in split_path[-1]:
        target_dir = "/".join(split_path[:-1])
    else:
        target_dir = destination
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    return shutil.copy2(str(image), destination)
