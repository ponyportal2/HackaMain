
from PIL import Image

import os



def picSize(path, max_size):
    img = Image.open(path)
    
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
    savePic(resized_img, path)
    img.close()


def savePic(resized_img, path):
    str = path.rsplit('.')
    l = len(str)
    formatIs = str[l-1]
    str = path.rsplit('.')

    str_names = path.rsplit('/')
    l_names = len(str_names)
    file_name = str_names[l_names - 1]
    onlypath = path.replace(file_name, "")

    avaName = 'thumb'
    partfile = os.path.join(onlypath, avaName)
    AvaPick = partfile +'.'+ formatIs
   
    resized_img.save(AvaPick)



def ava(usr, fileOrPath):

    start_directory = os.path.join('/usr/', usr)

    for root, _, files in os.walk(start_directory):
        if fileOrPath in files:
            absolute_path = os.path.join(root, fileOrPath)
            print(f"Файл {fileOrPath} найден по пути: {absolute_path}")
            picSize(absolute_path,200)
            break
    if not absolute_path:
        print(f"Файл {fileOrPath} не найден в заданной директории и её поддиректориях.")


