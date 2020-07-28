# funcs.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: contains functions and other things used by src/main.

import os
import sys
import time
import shutil
import logging
import requests
import validators
import multiprocessing
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime as dt
from pytube import YouTube, Playlist

# Achieve Playlists to be added to the stream

# Path definitions
ROOT_DIR = Path("../")
FFMPEG_URL = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200522-38490cb-win64-static.zip"
FFMPEG_INSTALLATION_DIR = ROOT_DIR / Path("ffmpeg")
ZIPPED_FFMPEG_PATH = FFMPEG_INSTALLATION_DIR / Path("ffmpeg.zip")
FFMPEG_BIN = FFMPEG_INSTALLATION_DIR / Path("bin")
IO_FOLDER_PATH = ROOT_DIR / Path("io")
IO_FOLDER_EXISTS = IO_FOLDER_PATH.exists()
LOGGER_OUT = ROOT_DIR / Path("log")
loggersToDisable = (
    "pytube.helpers", "pytube.extract",
    "pytube.cipher", "pytube.__main__",
    "pytube.streams"
)

# Disable unwanted loggers from Pytube.
for loggerName in loggersToDisable:
    loggerDisabling = logging.getLogger(loggerName)
    loggerDisabling.setLevel(50)

def ffmpegExists():
    ffmpegExistsInRoot = os.path.exists(FFMPEG_INSTALLATION_DIR)
    ffmpegExistsInPath = shutil.which("ffmpeg")

    if not ffmpegExistsInPath or not ffmpegExistsInRoot:
        return False
    return True
    
def setup():
    """Currently, all this function does is setup the envionment
        for the program to execute. It does:
        - Validation of an FFmpeg Installation
        - Adding this to the path (optional)
        - Generate data folders, incliding data/input, and
        data/output
    """

    # Create and download FFmpeg, and set up the files if there is no
    # EXE in the path, or in the root project directory.
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
    
    # Make folders that contain I/O stuff.
    if not ioFolderExists:
        print("[*] Data folder not detected.")
        os.mkdir(IO_FOLDER_PATH)
        os.mkdir(IO_FOLDER_PATH / Path("input"))
        os.mkdir(IO_FOLDER_PATH / Path("output"))

class Downloader():
    __conversionParams = {}
    __logger = None
    __state = "Paused"
    __states = ("Paused", "Stopped", "Playing", "Dead")

    def __init__(self, outputFolder, urls=[], logging=False):
        """Initiates the Downloader object.

            Args:
                outputFolder (string): The folder to output the final downloaded,
                or converted file.
        """

        self.isLoggingAllowed = logging
        self.outputFolder = outputFolder
        self.__urlStream = list(urls)

    def __convert(self, pathToFile):
        """Takes in a file from pathToFile, and then
        """

        if ffmpegExists:
            # Create a path without any extension.
            convertTo = self.__conversionParams["convertTo"]
            truePath = Path(pathToFile).parents[0] / Path(pathToFile).stem        
            os.system(f'ffmpeg -i "{truePath}.mp4" "{truePath}.{convertTo}"')

    def __log(self, message, level):
        if self.__logger:
            classLogger = self.__logger

            levels = {
                10: classLogger.debug,
                20: classLogger.info,
                30: classLogger.warning,
                40: classLogger.error,
                50: classLogger.critical
            }

            if levels.get(level):
                levels[level](message)

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

        self.__log(f"")

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
            self.__log(f"Set state of downloader to {state}.", 20)
            self.__state = state
        else:
            self.__log(f"Attempt to set invalid state, {state}.", 10)
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

        self.__log("Stream started.", 10)
        self.set_state("Playing")

    def pause_stream(self):
        """Pauses the stream. While this will stop the
            downloading and writing of a file, it will NOT
            stop the conversion of one. Instead, while
            conversion is happening, it will pause after the
            the file has finished converting.
        """

        self.__log("Stream paused.", 10)
        self.set_state("Paused")

    def stop_stream(self):
        """Stops the stream.
        """

        self.__log("Stream stopped..", 10)
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
                self.__log("Resuming downloader stream.", 20)

                # Start downloading the newest video
                if len(self.__urlStream) > 0:
                    video = YouTube(self.__urlStream[0])
                    videoStream = video.streams.first()
                    videoTitle = video.player_response["videoDetails"]["title"]
                    videoPath = videoStream.download(output_path=self.outputFolder, filename=videoTitle)
                    self.__log(f"Downloaded video {videoTitle} to path {videoPath}", 20)

                    if self.__conversionParams["enabled"] and ffmpegExists:
                        self.__convert(videoPath)

                    self.__urlStream.pop(0)
                else:
                    self.set_state("Paused")
        else:
            self.__log("Downloader has been killed during runtime.", 20)
            self.set_state("Dead")

    def config_conversion(self, enabled=False, convertTo="mp4"):
        """Configures the conversion (if enabled) of videos downloaded by this
        Downloader object. Can convert MP4 to anything FFmpeg supports. You can
        find these by doing "ffmpeg -formats" at your commandline.

        :param enabled: Whether or not conversion is enabled., defaults to False
        :type enabled: bool, optional
        :param convertTo: The format to convert to., defaults to "mp4"
        :type convertTo: string, optional
        """

        self.__conversionParams = {
            "enabled": enabled,
            "convertTo": convertTo,
        }

        self.__log("Successfully initiated conversion!", 20)

    def config_logger(self, loggingdDir="../log", loggerLevel=0):
        """Configures and sets up paramaters for the logging
            of this Downloader instance.

        Args:
            enabled (bool, optional): Whether or not logging is allowed. Defaults to False.
            loggingdDir (str, optional): The place where log files will be stored. Defaults to "../log".
            loggerLevel (int, optional): The minimum level to log. Defaults to 0.
        """

        logging.basicConfig(
            filename=str(Path(loggingdDir) / Path(dt.now().strftime("%Y-%m-%d"))),
            format="%(name)s %(levelname)s %(asctime)s - %(message)s",
            level=loggerLevel
        )

        self.__logger = logging.getLogger(__name__)
        self.__log("Logger successfully initiated.", 10)

def next_prog(max_num, scale):
    percent = round(scale / max_num * 100)
    prog_char, none_char = "=", " "
    total_prog = f"<{prog_char * percent}{none_char * (100-percent)}>"

    print(total_prog, end="\r")


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
    rint("\n" * position, end=f"{text}\n")
