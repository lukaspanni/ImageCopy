[![](https://img.shields.io/github/license/lukaspanni/ImageCopy.svg)](https://github.com/lukaspanni/ImageCopy/blob/master/LICENSE) 
[![](https://img.shields.io/github/v/release/lukaspanni/ImageCopy)](https://github.com/lukaspanni/ImageCopy/releases/latest) 
![Python application](https://github.com/lukaspanni/ImageCopy/workflows/Python%20application/badge.svg)

# ImageCopy

Tool for fast and easy copying of RAW/JPG images from a camera to a hard drive.

## Features

- Search and copy all image files automatically.
- Separate RAW and JPG images in different folders.
- Group images based on creation date. Group by:
    
    - Year
    - Month (either 1-12 or January-December)
    - Day


## Planned Features

- Automatic renaming


## Usage

### Create a config.yml file 

**Reccomendation:** rename the config.example.yml and adjust settings there.
   
Basic Config (copies all images from `input_dir` including all subdirectories to `output_dir`): 
```yaml
input-output:
    input_dir: /SD/DCIM/
    output_dir: /home/img/
    separate_raw: no
```
To create a separate folder for RAW-Images you have to set `separate_raw` to `yes` and provide a name for `raw_dir_name`.

Additionally there is the option to group images by creation date.
You can choose to group images based on **year**, **month** and/or **date**. 
If you choose to group by month you can enable `month_named`. This will create directories with the months name instead of its number.
The following example shows how to use the grouping-feature:
```yaml
grouping:
  year: yes
  month: yes
  month_named: yes
  day: no
```

The resulting directory structure will look something like this:
```
/
├── 2019
│   └── May
|       └── DSC00192.JPG
|       └── DSC00193.JPG
|   └── November
|       └── DSC01337.JPG
|       └── DSC01342.JPG
├── 2020
│   └── March
|       └── DSC00042.JPG
```
   
### Execute

If the configuration file is set up you can execute the `image_copy.py` script.
When the input and output directories stay the same and you don't want to group differently you can execute it as often as you want wihtout changing the config.
