#!/usr/bin/env python

from gimpfu import *
from os import listdir
from os.path import isfile, join

def RESIZE_QUICK(image, drawable, spriteWidth, spriteHeight):
    dir_path = "C:/Users/ribro/Dropbox/Phobos General/Equipment BACKUP2/xl/media/"
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    maxNewSize = 32
    
    for file in files:
        image = pdb.file_png_load(dir_path+file, dir_path+file)
        save_path = dir_path+"small/"+ file
        if (image.width > 100 or image.height > 100):
            minRatio = min(maxNewSize / float(image.width), maxNewSize / float(image.height))
            newWidth = image.width * minRatio
            newHeight = image.height * minRatio
            pdb.gimp_message("resizing... " + str(image.width) + ", " + str(image.height))
            pdb.gimp_image_scale_full(image, newWidth, newHeight, 0)
        else:
            pdb.gimp_message("NOT resizing... " + str(image.width) + ", " + str(image.height))
        pdb.file_png_save(image, image.active_drawable, save_path, save_path, 0, 0, 0, 0, 0, 0, 0)
        pdb.gimp_message(file)


register(
    "RESIZE-QUICK",
    "Resize individual sprite to a pre-defined size",
    "LONG DESCRIPTION",
    "Rob Willson", "RF", "2021",
    "Quick resize",
    "RGB*", # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
    [
        # basic parameters are: (UI_ELEMENT, "variable", "label", Default)
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_SLIDER, "spriteWidth", "Sprite width", 64, (32, 128, 32)),
        (PF_SLIDER, "spriteHeight", "Sprite height", 64, (32, 128, 32))
    ],
    [],
    RESIZE_QUICK, menu="<Image>/Tools/Spritesheets")  # second item is menu location

main()