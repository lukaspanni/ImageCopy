import os
from pathlib import Path
from typing import Union

from ImageCopy.image_file import ImageFile


class ImageFinder:
    @staticmethod
    def get_images(directory: Union[str, Path], target_dir: Union[str, Path], filter_extensions: list = None) -> dict:
        """
        Uses _get_image_list to get a list of all images and converts it into a dictionary
        :param directory: image source
        :param target_dir: output directory
        :param filter_extensions: filter files by specific extensions. If None specified files are filtered by standard
                RAW and JPG extensions
        :return: dictionary of ImageFile objects and output paths
        """
        if filter_extensions is None:
            filter_extensions = ImageFile.raw_extensions + ImageFile.image_extensions
        image_list = ImageFinder._get_image_list(directory, filter_extensions)
        return dict.fromkeys(image_list, target_dir)

    @staticmethod
    def _get_image_list(directory: Union[str, Path], filter_extensions: list) -> list:
        """
        Recursively loads a list of all image files in the specified directory or any subdirectory.
        :param directory: start searching for image files here
        :param filter_extensions: filter files by specific extensions. If None specified files are filtered by standard
                RAW and JPG extensions
        :return: list of ImageFile objects
        """
        files = []
        for entry in Path(directory).iterdir():
            if entry.is_file():
                if filter_extensions is not None:
                    _, ext = os.path.splitext(str(entry))
                    ext = ext.lower()
                    if ext in filter_extensions:
                        files.append(ImageFile(entry, ext))
                else:
                    files.append(entry)
            else:
                files += ImageFinder._get_image_list(entry, filter_extensions)
        return files
