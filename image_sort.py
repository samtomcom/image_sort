import sys
import os
import hashlib
from PIL import Image  # uses pillow
import shutil

#rootdir = sys.argv[1]
rootdir = '/media/clint/libraries/pictures/wallpapers'
inputdir = os.path.join(rootdir,'in')
outputdir = os.path.join(rootdir, 'out')

print(inputdir)

# md5 checksum of file
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def gen_dict():
    file_dict = {}
    for subdir, dirs, files in os.walk(inputdir):
        for file in files:
            full_path = os.path.join(inputdir, subdir, file)
            check = md5(full_path)
            im = Image.open(full_path)
            x, y = im.size
            if check not in file_dict:
                file_dict[check] = [file, full_path, x, y]
            else:
                print("Skipping duplicate file: {}".format(full_path))
    return file_dict

def copy(file_dict):
    aspect_ratios = {1.3: "1.33_4x3",
                     1.8: "1.78_16x9",
                     1.0: "1.00_1x1"
    }

    for check in file_dict:
        file, full_path, x, y = tuple(file_dict[check])
        aspect_r = round(float(x)/y, 1)
        aspect_path = os.path.join(outputdir, str(aspect_r))
        if aspect_r in aspect_ratios:
            aspect_path = os.path.join(outputdir, aspect_ratios[aspect_r])

        if not os.path.exists(aspect_path):
            os.makedirs(aspect_path)

        new_path = os.path.join(aspect_path, file)
        if not os.path.exists(new_path):
            shutil.copyfile(full_path, new_path)



copy(gen_dict())
