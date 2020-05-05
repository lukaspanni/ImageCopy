import os

import piexif
import yaml

from grouper import GroupBy, Grouper
from image_copier import ImageCopier, RAWSeparateImageCopier
from image_file import ImageFile


# https://stackoverflow.com/a/34325723
# Print iterations progress
def progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=end)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":
    config_file = "config.yml"
    if not os.path.exists(config_file):
        print("Config file", config_file, "not found.")
        exit(-1)

    with open(config_file, "r") as yml:
        cfg = yaml.load(yml, Loader=yaml.SafeLoader)

    if 'input-output' not in cfg:
        print("Error in config file")
        exit(-1)

    if 'input_dir' not in cfg['input-output'] or not os.path.exists(cfg['input-output']['input_dir']):
        print("Input directory not found")

    grouping = None
    if 'grouping' in cfg:
        group_by = set()
        if 'year' in cfg['grouping'] and cfg['grouping']['year']:
            group_by.add(GroupBy.YEAR)
        if 'month' in cfg['grouping'] and cfg['grouping']['month']:
            if 'named_named' in cfg['grouping'] and cfg['grouping']['months_named']:
                group_by.add(GroupBy.MONTH_NAMED)
            else:
                group_by.add(GroupBy.MONTH)
        if 'day' in cfg['grouping'] and cfg['grouping']['day']:
            group_by.add(GroupBy.DAY)
        grouping = Grouper(group_by)

    if 'exif' in cfg:
        exif_tags = dict()
        if 'artist' in cfg['exif']:
            exif_tags[piexif.ImageIFD.Artist] = cfg['exif']['artist']
        if 'copyright' in cfg['exif']:
            exif_tags[piexif.ImageIFD.Copyright] = cfg['exif']['copyright']

    if 'separate_raw' in cfg['input-output'] and cfg['input-output']['separate_raw']:
        copier = RAWSeparateImageCopier(cfg['input-output']['output_dir'], cfg['input-output']['raw_dir_name'], grouping)
    else:
        copier = ImageCopier(cfg['input-output']['output_dir'], grouping)

    images = ImageFile.get_images(cfg['input-output']['input_dir'])

    i = 0
    progress_bar_length = len(images)
    print("Copying images from", cfg['input-output']['input_dir'], "to", cfg['input-output']['output_dir'])
    progress_bar(i, progress_bar_length, prefix="Progress:", suffix="Complete", length=50, end="")
    for image in images:
        i += 1
        progress_bar(i, progress_bar_length, prefix="Progress:", suffix="Complete", length=50, end="")
        try:
            copier.copy(image)
        except PermissionError as pe:
            print("\n", pe) # TODO: Error handling

    print("All images copied.")
