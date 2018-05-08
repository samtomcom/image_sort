import sys
import os
import hashlib
from PIL import Image  # uses pillow

#rootdir = sys.argv[1]
rootdir = '/media/clint/libraries/pictures'
inputdir = os.path.join(rootdir,'test_in')
outputdir = os.path.join(rootdir, 'test_out')

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
            print(file)
            full_path = os.path.join(inputdir, subdir, file)
            check = md5(full_path)
            im = Image.open(full_path)
            x, y = im.size
            file_dict[check] = [file, full_path, x, y]
    return file_dict

print(gen_dict())

