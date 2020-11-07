*********
Overview
*********

Tool for fast and easy copying of RAW/JPG images from a camera to a hard drive.

Features (version 2.0)
======================

* Search and copy all image files automatically.
* Separate RAW and JPG images in different folders.
* Group images based on creation date. Group by:
    
    * Year
    * Month (either 1-12 or January-December)
    * Day

* Set EXIF Data in JPG images (artist and copyright)
* Create a greyscale copy of JPG images

Planned Features
================

* Automatic renaming


Usage
=====

Create a config.yml file
------------------------

**Reccomendation:** rename the config.example.yml and adjust settings there.
   
**Module config:** list of modules to use.
.. code-block::

    modules:
      - grouping
      - raw_separate
      - exif
      - greyscale

  
Basic Config (copies all images from `input_dir` including all subdirectories to `output_dir`): 
.. code-block::

    input-output:
      input_dir: /SD/DCIM/
      output_dir: /home/img/


Modules
--------

Currently (Version 2.0) available: 

* grouping
    Group images by creation date.
    You can choose to group images based on **year**, **month** and/or **date**.
    If you choose to group by month you can enable ``month_named``. This will create directories with the months name instead of its number.
    The following example shows how to use the grouping-feature:

    .. code-block::

        grouping:
          year: yes
          month: yes
          month_named: yes
          day: no


    The resulting directory structure will look something like this:
     
    .. code-block::

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


* raw_separate
    
    Separate RAW Images in different directory specified by ``raw_dir_name``. Example usage:
    .. code-block::

        raw_separate:
          separate_raw: yes
          raw_dir_name: RAW

    
* exif
    
    Set Artist and Copyright in JPG images, RAW images are not affected. Example usage:
    
    .. code-block::

        exif:
          artist: Lukas Panni
          copyright: Lukas Panni

    
* greyscale

    Create a greyscale copy of every JPG image. Can use one of three different algorithms (average, luminosity, lightness) default: average.
    ``file_name`` specifies a string that is appended to the original file name to identify the greyscale copy.

    .. code-block::

        greyscale:
          algorithm: average
          file_name: greyscale




Execute
-------

If the configuration file is set up you can execute the ``image_copy.py`` script or the bundled executable for your platform.
When the input and output directories stay the same and you don't want to group differently you can execute it as often as you want wihtout changing the config.
