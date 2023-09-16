
from PIL import Image

import os

def picSize(path_in, path_out, max_size):
    img = Image.open(path_in)
    
    oldW = img.width
    oldH = img.height 
    if oldH < oldW:
        scale_percent = (max_size / oldW )
    elif oldH > oldW:
        scale_percent = (max_size / oldH )
    else:
        scale_percent = (max_size / oldH )

    new_width = int(oldW * scale_percent) 
    new_height = int(oldH * scale_percent)

    dsize = (new_width, new_height)

    resized_img = img.resize(dsize, Image.LANCZOS)
    resized_img.save(path_out)
    img.close()

def create_thumb(filename):
    if not os.path.exists('thumb'):
        os.makedirs('thumb')
    picSize(filename, convert_to_thumb_path(filename),200)

def convert_to_thumb_path(original_path):
    directory = os.path.dirname(original_path)
    thumb_directory = os.path.join(directory, "thumb")

    if not os.path.exists(thumb_directory):
        os.makedirs(thumb_directory)

    thumb_path = os.path.join(thumb_directory, os.path.basename(original_path))
    return thumb_path