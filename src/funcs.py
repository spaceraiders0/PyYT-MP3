# funcs.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: contains functions and other things used by src/main.

import os
import requests
import validators
import sys
import shutil
import time
from pathlib import Path
from zipfile import ZipFile

ROOT_DIR = Path("../")
FFMPEG_URL = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200522-38490cb-win64-static.zip"
FFMPEG_INSTALLATION_DIR = ROOT_DIR / Path("ffmpeg")
ZIPPED_FFMPEG_PATH = FFMPEG_INSTALLATION_DIR / Path("ffmpeg.zip")
DATA_FOLDER_PATH = ROOT_DIR / Path("data")

logging_enabled = False

def setup():
    """Currently, all this function does is setup the envionment
    for the program to execute. It does:
        - Validation of an FFmpeg Installation
        - Adding this to the path (optional)
        - Generate data folders, incliding data/input, and
        data/output
    """

    ffmpeg_exists = os.path.exists(FFMPEG_INSTALLATION_DIR)
    data_folder_exists = os.path.exists(DATA_FOLDER_PATH)

    # Create and download FFmpeg, and set up the files.
    if not ffmpeg_exists:
        print("[*] FFmpeg installation undetected, installing.")
        os.mkdir(FFMPEG_INSTALLATION_DIR)
        zipped_data = requests.get(FFMPEG_URL).content

        # Write the bytes of the downloaded .ZIP to a new file.
        with open(ZIPPED_FFMPEG_PATH, "ab") as zipfile_data:
            zipfile_data.write(zipped_data)

        # Extract the .ZIP's contents.
        with ZipFile(ZIPPED_FFMPEG_PATH) as zipped_file:
            zipped_file.extractall(path=FFMPEG_INSTALLATION_DIR)

        # Extract the contents of the subfolder, where all the actual files are.
        subfolder_name = os.path.split(FFMPEG_URL)[1].strip(".zip")
        subfolder = FFMPEG_INSTALLATION_DIR / Path(subfolder_name)

        for dirpath, dirnames, filenames in os.walk(subfolder):
            # loop through a list of all the items instead of two
            # seperate loops for files and directories
            directory_items = dirnames + filenames

            # Move all the files and folders
            for item in directory_items:
                shutil.move(str(subfolder / Path(item)),
                            str(FFMPEG_INSTALLATION_DIR))

        # No need for the original .ZIP file, or the extracted folder.
        os.remove(ZIPPED_FFMPEG_PATH)
        os.rmdir(subfolder)
    else:
        print("[*] FFmpeg installation detected!")

    # Make folders that contain I/O stuff.
    if not data_folder_exists:
        print("[*] Data folder not detected.")
        os.mkdir(DATA_FOLDER_PATH)
        os.mkdir(DATA_FOLDER_PATH / Path("input"))
        os.mkdir(DATA_FOLDER_PATH / Path("output"))
    else:
        print("[*] Data folder detected.")

def next_prog(max_num, scale):
    percent = round(scale / max_num * 100)
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

def validate_url(url, insertion=None):
    """
        This function will determine whether or not the URL
        provided matches formatting for an actual URL.

        Arguments:
            url {string} -- The URL to be validated

        Keyword Arguments:
            insertion {list} -- Where the URL will be inserted into (default: {None})

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


def cls():
    """Simply clears the screen, in a multi-platform way.
    """

    system = sys.platform

    if system == "win32":
        os.system("cls")
    elif system in ("darwin", "linux"):
        os.system("clear")


def draw_at_row(text, percent=0):
    """Draws text at the specified % of the screen rows. It does this by
    wiping the screen, and then generating a bunch of newlines based off the
    percent argument.

    Args:
        text (string): The text to draw on the screen.
        percent (integer, optional): the % of the screen to draw at. Defaults to 0.
    """

    cls()
    columns = round(shutil.get_terminal_size().columns / 4)
    position = round(columns * percent / 100)
    print("\n" * position, end=f"{text}\n")
