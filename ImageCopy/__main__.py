import sys
import image_copy

# TODO: add input validation
if len(sys.argv) > 2: 
    config_file = sys.argv[1]
    image_copy.main(config_file)
else:
    print('No config specified')