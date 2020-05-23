# funcs.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: contains functions and other things used by src/main.

import os
from pathlib import Path

root_dir = os.path.abspath(Path("../.."))
print(root_dir)


def validate_ffmpeg_install():
    """
        Checks whether or not ffmpeg is downloaded into this current directory.
        If it is not, it will install it and extract it's contents into the
        PyYT folder.
    """

    if os.path.isdir(Path("")):
        pass
