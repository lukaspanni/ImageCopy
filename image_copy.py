import os
import yaml


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

    if not os.path.exists(cfg['input-output']['input_dir']):
        print("Input directory", cfg['input-output']['input_dir'], "not found")

    if cfg['input-output']['separate_raw']:
        copier = RAWSeparateImageCopier(cfg['input-output']['output_dir'], cfg['input-output']['raw_dir_name'])
    else:
        copier = ImageCopier(cfg['input-output']['output_dir'])

    images = ImageFile.get_images(cfg['input-output']['input_dir'])

    i = 0
    progress_bar_length = len(images)
    print("Copying images from", cfg['input-output']['input_dir'], "to", cfg['input-output']['output_dir'])
    progress_bar(i, progress_bar_length, prefix="Progress:", suffix="Complete", length=50, end="")
    for image in images:
        i += 1
        progress_bar(i, progress_bar_length, prefix="Progress:", suffix="Complete", length=50, end="")
        copier.copy(image)
    print("All images copied.")
