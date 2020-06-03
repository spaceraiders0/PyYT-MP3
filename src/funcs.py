# funcs.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: contains functions and other things used by src/main.

import os, requests, validators
from pathlib import Path

ROOT_DIR = Path("../..")
FFMPEG_URL = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200522-38490cb-win64-static.zip"

def next_prog(max_num, scale):
    percent = round(scale/max_num*100)
    prog_char, none_char = "=", " "
    total_prog = f"<{prog_char * percent}{none_char * (100-percent)}>"

    print(total_prog, end="\r")


def recursive_dir_get(match, attempts=10):
    """This function will recursively go up a level in the
    directory structure and attempt to match a directory name
    with match.

    Arguments:
        match {string} -- The directory name to attempt to match.

    Keyword Arguments:
        attempts {int} -- The maximum amount of attempts to match. (default: {10})

    Returns:
        string -- The path to the matched directory.
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
        return ""


def validate_ffmpeg_install():

    if os.path.isdir(Path("")):
        print("jkjj")


def validate_url(url, insertion=None):
    """
        This function will determine whether or not the URL
        provided matches formatting for an actual URL.

        Arguments:
            url {string} -- The URL to be validated

        Keyword Arguments:
            insertion {list} --  Where the URL will be inserted into (default: {None})

        Returns:
            bool -- The validity of the URL.
    """

    # validators.url returns a boolean when it's a valid url,
    # and a tuple when it's not.
    if isinstance(validators.url(url), bool):
        if insertion is not None:
            insertion.append(url.strip("\n"))
        return True
    else:
        return False
