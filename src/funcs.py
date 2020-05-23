# funcs.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: contains functions and other things used by src/main.

import os
import requests
from pathlib import Path

ROOT_DIR = Path("../..")
FFMPEG_URL = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200522-38490cb-win64-static.zip"


def recursive_dir_get(match, attempts=10):
    """
        Will return the path of a parent directory denoted by
        match.
    """

    total_attempts = 0

    while total_attempts <= attempts:
        current_directory = os.path.basename(os.path.abspath("."))

        if current_directory == match:
            os.chdir(__file__)
            return os.abspath(current_directory)

        os.chdir("..")
        total_attempts += 1
    else:
        return None

def validate_ffmpeg_install():
    """
        Checks whether or not ffmpeg is downloaded into this current directory.
        If it is not, it will install it and extract it's contents into the
        PyYT folder.
    """

    if os.path.isdir(Path("")):
        print("jkjj")
