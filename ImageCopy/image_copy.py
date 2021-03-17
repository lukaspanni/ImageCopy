"""
Main module for ImageCopy
"""
from ImageCopy.image_finder import ImageFinder
from ImageCopy.action_runner import ActionRunner
from ImageCopy.config import Config
from ImageCopy.copier import Copier
from multiprocessing import Process, Queue

CONFIG_FILE = "config.yml"


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
    pr_bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, pr_bar, percent, suffix), end=end)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == "__main__":
    config = Config(CONFIG_FILE)
    images = ImageFinder.get_images_dict(config.io.input_dir, config.io.output_dir)
    runner = ActionRunner(config)
    runner.execute_transformers(images)

    after_copy_actions = runner.get_after_action_count() > 0
    after_copy_queue = Queue()
    feedback_queue = Queue()
    if after_copy_actions:
        after_copy_process = Process(target=runner.after_action_process,
                                     args=(runner.after_actions, after_copy_queue, feedback_queue))
        after_copy_process.start()


    i = 0
    print("Copying images from", config.io.input_dir, "to", config.io.output_dir)
    progress_bar(i, len(images), prefix="Progress:", suffix="Complete", length=50, end="")
    copier = Copier(config)
    for image in images:
        i += 1
        progress_bar(i, len(images), prefix="Progress:", suffix="Complete", length=50, end="")
        try:
            images[image] = copier.copy(image, images[image])
            if after_copy_actions:
                after_copy_queue.put({image: images[image]})
        except PermissionError as per:
            print("\n", per)  # TODO: Error handling
    after_copy_queue.put("END")
    print("All images copied.")

    if not after_copy_actions:
        exit()

    print("Executing after copy actions")
    while not (counter := feedback_queue.get()) == "END":
        progress_bar(counter, len(images), prefix="Progress:", suffix="Complete", length=50, end="")

    # runner.execute_after_actions(images, add_progress)
