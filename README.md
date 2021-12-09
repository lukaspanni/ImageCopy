[![](https://img.shields.io/github/license/lukaspanni/ImageCopy.svg)](https://github.com/lukaspanni/ImageCopy/blob/master/LICENSE) 
[![](https://img.shields.io/github/v/release/lukaspanni/ImageCopy)](https://github.com/lukaspanni/ImageCopy/releases/latest) 
![Python application](https://github.com/lukaspanni/ImageCopy/workflows/Python%20application/badge.svg)

# ImageCopy

Tool for fast and easy copying of RAW/JPG images from a camera to a hard drive.

## Features (version 2.1)

- Features of version 2.0 (Greyscale is disabled in the release but can be enabled if built from source)
- Configuration for already existing Files
    - Always overwrite: silently overwrite already existing files
    - Never overwrite: silently ignore already existing files
    - Warn: overwrite already existing files, but warn user that files are overwritten
    - Append Suffix: append a suffix to files with the same filename

## Features (version 2.0)

- Search and copy all image files automatically.
- Separate RAW and JPG images in different folders.
- Group images based on creation date. Group by:
    
    - Year
    - Month (either 1-12 or January-December)
    - Day

- Set EXIF Data in JPG images (artist and copyright)
- Create a greyscale copy of JPG images (just for fun, not really a useful feature :smile:)

## Planned Features

- Automatic renaming


## Usage

### Create a config.yml file 

**Recommendation:** rename the config.example.yml and adjust settings there.
   
**Module config:** list of modules to use.
````yaml
modules:
  - grouping
  - raw_separate
  - exif
````
  
Basic Config (copies all images from `input_dir` including all subdirectories to `output_dir`): 
```yaml
input-output:
  input_dir: /SD/DCIM/
  output_dir: /home/img/
```

Copy-Configuration (configures handling of already existing files in output_dir)
```yaml
copy:
  mode: append-suffix
```

Available Config-Options:

- "always-overwrite": silently overwrite already existing files
- "warn-before-overwrite": overwrite already existing files, but warn user that files are overwritten
- "never-overwrite": silently ignore already existing files
- "append-suffix": append a suffix to files with the same filename

#### Modules

Currently (Version 2.1) available: 

- grouping 
    
    Group images by creation date.
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
       
- raw_separate
    
    Separate RAW Images in different directory specified by `raw_dir_name`. Example usage:
    ````yaml
    raw_separate:
      separate_raw: yes
      raw_dir_name: RAW
    ````
    
- exif
    
    Set Artist and Copyright in JPG images, RAW images are not affected. Example usage:
    
    ```yaml
    exif:
      artist: Lukas Panni
      copyright: Lukas Panni
    ```
    
- greyscale

    Create a greyscale copy of every JPG image. Can use one of three different algorithms (average, luminosity, lightness) default: average.
    `file_name` specifies a string that is appended to the original file name to identify the greyscale copy.

    ```yaml
    greyscale:
      algorithm: average
      file_name: greyscale
    ```




### Execute

If the configuration file is set up you can execute the `image_copy.py` script or the bundled executable for your platform.
When the input and output directories stay the same and you don't want to group differently you can execute it as often as you want wihtout changing the config.
