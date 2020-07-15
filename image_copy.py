from GroupingTransform import GroupingTransform
from ImageFinder import ImageFinder
from RawSeparateTransform import RawSeparateTransform
from config import Config
from image_copier import copy


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
    config = Config(config_file)
    images = ImageFinder.get_images(config.io.input_dir, config.io.output_dir)

    i = 0
    progress_bar_length = len(images)
    print("Copying images from", config.io.input_dir, "to", config.io.output_dir)
    progress_bar(i, progress_bar_length, prefix="Progress:", suffix="Complete", length=50, end="")
    for image in images:
        i += 1
        progress_bar(i, progress_bar_length, prefix="Progress:", suffix="Complete", length=50, end="")
        try:
            copy(image, images[image])
        except PermissionError as pe:
            print("\n", pe)  # TODO: Error handling

    print("All images copied.")
