"""
Exif-Editing Feature
"""
import piexif

from ImageCopy.Actions.after_copy_action import AfterCopyAction


def _load_exif_config(config: dict):
    """
    Load exif-config and create dict of exif-tags
    """
    exif = dict()
    if 'artist' in config:
        exif[piexif.ImageIFD.Artist] = config['artist']
    if 'copyright' in config:
        exif[piexif.ImageIFD.Copyright] = config['copyright']
    return exif


class ExifEditing(AfterCopyAction):
    """
    Sets Exif-Data in copied Images
    """

    def __init__(self, exif_data: dict):
        self.exif_data = _load_exif_config(exif_data)

    def set_exif_data(self, image: str):
        """
        Sets exif data in Image.
        Currently only for JPGs.
        :param image: Path to image
        """
        exif = piexif.load(image)
        for key in self.exif_data:
            exif['0th'][key] = self.exif_data[key]
        exif_bytes = piexif.dump(exif)
        piexif.insert(exif_bytes, image)

    def execute(self, images: dict):
        for img in images:
            if not img.is_raw():
                self.set_exif_data(images[img])
