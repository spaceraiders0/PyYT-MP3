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
import multiprocessing
import logging
from datetime import datetime as dt
from pathlib import Path
from zipfile import ZipFile
from pytube import YouTube, Playlist

# Achieve Playlists to beadded to the stream

# Path definitions
ROOT_DIR = Path("../")
FFMPEG_URL = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200522-38490cb-win64-static.zip"
FFMPEG_INSTALLATION_DIR = ROOT_DIR / Path("ffmpeg")
ZIPPED_FFMPEG_PATH = FFMPEG_INSTALLATION_DIR / Path("ffmpeg.zip")
IO_FOLDER_PATH = ROOT_DIR / Path("io")
LOGGER_OUT = ROOT_DIR / Path("log")

class Downloader():
    __loggingParams = {}
    __conversionParams = {}
    __logger = None
    __state = "Paused"
    __states = ("Paused", "Stopped", "Playing", "Dead")

    def __init__(self, outputFolder, urls=[]):
        """Initiates the Downloader object.

            Args:
                outputFolder (string): The folder to output the final downloaded,
                or converted file.
        """

        self.outputFolder = outputFolder
        self.__urlStream = list(urls)

    def __log(self, message, level):
        """Logs a message to a logger file if
            self.allowLogging is True.

            Args:
                message (string): The message to log.
                level (int): The level of message to log.
                Can be either an integer, or one of the
                constants provided by the logging module.
        """
        currentTime = str(time.time())

        if self.allowLogging:
            # Make sure there's a "logging" directory here.

            # Setup the logger.
            if not self.logger:
                logging.basicConfig(
                    filename=str(LOGGER_OUT / Path(currentTime)),
                    format="%(levelname)s %(asctime)s - %(message)s")
                self.__logger = logging.getLogger()

    def __convert(self, pathToFile):
        """Takes in a file from pathToFile, and then
            converts it based off self.conversionParams.
            While this method may be ran, no conversion
            will actually take place unless it is allowed
            by self.conversionParams.

            Args:
                pathToFile (string, pathlike): The path to the file
                that will be converted.
        """

        pass

    def add_to_stream(self, url):
        """Takes in a single URL, or list of URLs, and
            appends them to this Downloader stream. Validates
            that all URLs are properly formatted.

            Args:
                url (string, list): The URL(s) to add to the
                Downloader's stream.
        """

        urlsToAdd = list(url)

        # Filter out any invalid URLs
        for url in urlsToAdd:
            if not validators.url(url):
                urlsToAdd.remove(url)
                print("Detected invalid URL.")

        self.__urlStream += urlsToAdd

    def remove_from_stream(self, url):
        """Takes in a single URL to remove from the stream
            of URLs used by the Downloader.

            Args:
                url (string): The URL to remove from the stream.
        """

        if url in self.__urlStream:
            self.__urlStream.remove(url)

    def set_state(self, state):
        if state in self.__states:
            self.__state = state
        else:
            raise NameError("Invalid state") 

    def get_state(self):
        """Returns the current state of the downloader.

            Returns:
                string: The state of the downloader.
        """

        return self.__state

    def start_stream(self):
        """Starts the stream.
        """

        self.set_state("Playing")

    def pause_stream(self):
        """Pauses the stream. While this will stop the
            downloading and writing of a file, it will NOT
            stop the conversion of one. Instead, while
            conversion is happening, it will pause after the
            the file has finished converting.
        """

        self.set_state("Paused")

    def stop_stream(self):
        """Stops the stream.
        """

        self.set_state("Stopped")

    def get_stream(self):
        """Returns the current stream the Downloader is
           using.
        """

        return self.__urlStream

    def run(self):
        # Once stopped, the downloader will be "dead."
        while self.get_state() != "Stopped":

            # If it's unpaused, it wont do anything until it's unpaused.
            if self.get_state() == "Playing":

                # Start downloading the newest video
                if len(self.__urlStream) > 0:
                    video = YouTube(self.__urlStream[0])
                    videoStream = video.streams.first()
                    videoTitle = video.player_response["videoDetails"]["title"]
                    videoStream.download(output_path=self.outputFolder, filename=videoTitle)
                    self.__urlStream.pop(0)
                else:
                    self.set_state("Paused")
        else:
            self.set_state("Dead")

    def config_conversion(self, enabled=False, convertFrom=None, convertTo=None):
        """Configures settings for when conversion is to be
            done on downloaded files.

            Args:
                enabled (bool, optional): Whether or not conversion should
                                        happen. Defaults to False.
                convertFrom (string, optional): Filetype being converted.
                                                Defaults to None.
                convertTo (string, optional): Filetype to convert to. Defaults
                                            to None.
        """

        conversionParams = {
            "enableConversion": enabled,
            "convertFrom": convertFrom,
            "convertTo": convertTo,
        }

    def config_logger(self, enabled=False, loggingdDir="./log"):
        """Configures and sets up paramaters for the logging
            of this specific class.

            Args:
                enabled (bool, optional): Whether or not logging is enabled. Defaults to False.
                loggingdDir (str, optional): The output of the logger. Defaults to "./log".
        """

        loggingParams = {
            "allowLogging": enabled,
            "loggingDir": loggingdDir
        }


def setup():
    """Currently, all this function does is setup the envionment
        for the program to execute. It does:
        - Validation of an FFmpeg Installation
        - Adding this to the path (optional)
        - Generate data folders, incliding data/input, and
        data/output
    """

    ffmpegExists = os.path.exists(FFMPEG_INSTALLATION_DIR)
    ioFolderExists = os.path.exists(IO_FOLDER_PATH)

    # Create and download FFmpeg, and set up the files.
    if not ffmpegExists:
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
    if not ioFolderExists:
        print("[*] Data folder not detected.")
        os.mkdir(IO_FOLDER_PATH)
        os.mkdir(IO_FOLDER_PATH / Path("input"))
        os.mkdir(IO_FOLDER_PATH / Path("output"))
    else:
        print("[*] Data folder detected.")


def next_prog(max_num, scale):
    percent = round(scale / max_num * 100)
    prog_char, none_char = "=", " "
    total_prog = f"<{prog_char * percent}{none_char * (100-percent)}>"

    print(total_prog, end="\r")


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
        return {}


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
