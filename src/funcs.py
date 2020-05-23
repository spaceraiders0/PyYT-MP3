# funcs.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: contains functions and other things used by src/main.

import os
from pathlib import Path

root_dir = Path("../..")


# try to finish this tomorrow?
def recursive_dir_get(name):
    found_dir = False
    path = Path("")

    while not found_dir:
        new_path = path / Path("..")
        parent_name = os.path.basename(os.path.abspath(path))  
        #print(new_path)
        print(parent_name)
        break
        if parent_name == name:
            found_dir = True
            print(os.path.abspath(path))
        else:
            path /= Path("../")

def validate_ffmpeg_install():
    """
        Checks whether or not ffmpeg is downloaded into this current directory.
        If it is not, it will install it and extract it's contents into the
        PyYT folder.
    """

    if os.path.isdir(Path("")):
        print("jkjj")
