import os
import shutil
import time
from enum import Enum
from typing import final

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
            if (mode := config.copy["mode"]) is not None:
                try:
                    self.mode = Copier.OverwriteOptions(mode)
                    # if self.mode == Copier.OverwriteOptions.APPEND_SUFFIX:
                    #     if config.copy["suffix"] is not None:
                    #         self.suffix = config.copy["suffix"]
                    #     else:
                    #         self.suffix = str(int(time.time()))
                except ValueError:
                    print("Provided Copy-Mode", config.copy["mode"], "is not valid. Using 'always-overwrite'")
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
            final_destination = destination
        else:
            target_dir = destination
            final_destination = os.path.join(target_dir, image.get_filename())
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        # Check Overwrite Mode, TODO: Consider polymorphic implementation (especially if implementation changes)
        if self.mode == Copier.OverwriteOptions.WARN:
            # WARN
            if os.path.exists(final_destination):
                print("\nOverwriting Image", final_destination)

        if self.mode == Copier.OverwriteOptions.APPEND_SUFFIX:
            # TODO: Add Incremental Suffixes
            if os.path.exists(final_destination):
                final_destination = final_destination[:-len(image.extension)] + "_" + str(int(time.time())) + image.extension
        if self.mode == Copier.OverwriteOptions.NO_OVERWRITE:
            if os.path.exists(final_destination):
                return None

        return shutil.copy2(str(image), final_destination)
