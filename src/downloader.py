# downloader.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: contains the downloader object, and other things
# used by src/downloader.py

import os
import sys
import shutil
import logging
import textwrap
import requests
import validators
from pathlib import Path
from pytube import YouTube
from zipfile import ZipFile

# Path definitions
ROOT_DIR = Path(__file__).parent.absolute().parent
FFMPEG_URL = "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200522-38490cb-win64-static.zip"
INSTALLATION_DIRECTORY = ROOT_DIR / Path("ffmpeg")
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
    """Checks whether an FFmpeg installation can be located
    in the root directory, or somewhere in the PATH.

    :return: The command to be used to invoke FFmpeg, or False to signify
    that there was no installation found.
    :rtype: str, bool
    """
    ffmpegExistsInRoot = INSTALLATION_DIRECTORY.exists()
    ffmpegExistsInPath = shutil.which("ffmpeg")

    # Give different commands that're used to actually invoke FFmpeg.
    if ffmpegExistsInRoot:
        return str(ROOT_DIR / Path("ffmpeg.exe"))
    elif ffmpegExistsInPath:
        return "ffmpeg"

    return False


def setup():
    """Sets up FFmpeg by extracting the exe from a zipfile containing
    the FFmpeg installation.
    """

    if not ffmpegExists():
        ZIPFILE_LOCATION = ROOT_DIR / Path("ffmpeg.zip")
        ffmpeg_zip = requests.get(FFMPEG_URL)

        # Write individual chunks of bytes to a new zip file.
        with open(ZIPFILE_LOCATION, "wb") as new_zip_file:
            for chunk in ffmpeg_zip.iter_content(chunk_size=255):
                new_zip_file.write(chunk)

        # Extract the ZipFile
        with ZipFile(ZIPFILE_LOCATION) as zip_file:
            zip_file.extractall(INSTALLATION_DIRECTORY)

        # Extract the exe from the folder based off the stem
        # (the actual name of the URL without the file extension),
        shutil.move(str(INSTALLATION_DIRECTORY / Path(f"{Path(FFMPEG_URL).stem}/bin/ffmpeg.exe")), ROOT_DIR)

        # Recursively go through all files in ffmpeg, and delete them.
        Path(ROOT_DIR / Path("ffmpeg.zip")).unlink()
        shutil.rmtree(ROOT_DIR / Path("ffmpeg"))


class Downloader():
    """The Downloader object utilizes PyTube's video downloading to
    create a stream of videos that can be downloaded and converted
    into a specified format (assuming you have FFmpeg installed), and
    to a special location. It can be started, stopped, and paused, and
    can even have the stream it's using be modified as it's running.
    """

    __conversionParams = {}
    __logger = None
    __state = "Paused"
    __states = ("Paused", "Stopped", "Playing", "Dead")

    def __init__(self, outputFolder=".", urls=[], logging=False, killAfterFinished=False,
                 keepFile=False):

        """Initializes the downloader object.
        """

        self.outputFolder = outputFolder
        self.__urlStream = list(urls)
        self.isLoggingAllowed = logging
        self.killAfterFinished = killAfterFinished
        self.keepFile = keepFile

    def __convert(self, pathToFile: str):
        """Does the actual work to convert a file to a specified format.
        This method is only called when FFmpeg is installed, inside the
        run method.

        :param pathToFile: The path of the file to convert.
        :type pathToFile: str
        """

        cmdToUse = ffmpegExists()

        # Create a path without any extension.
        convertTo = self.__conversionParams["convertTo"]
        truePath = Path(pathToFile).parents[0] / Path(pathToFile).stem
        os.system(f'{cmdToUse} -i "{truePath}.mp4" "{truePath}.{convertTo}" -loglevel warning')

        if not self.keepFile:
            os.remove(f"{truePath}.mp4")

    def add_to_stream(self, urls: list):
        """Takes in a single URL, or list of them, and filters them
        for invalid URLs, then appends them to the stream.

        :param url: A list of URLs to be appended to the stream.
        :type url: list
        """

        # Filter out any invalid URLs
        for url in urls:
            if validators.url(url):
                self.__urlStream += url

    def remove_from_stream(self, url: str):
        """Removes a URL from the stream.

        :param url: The URL to remove from the stream.
        :type url: str
        """

        if url in self.__urlStream:
            self.__urlStream.remove(url)

    def set_state(self, state: str):
        """Sets the current state of the Downloader.

        :param state: The state to change the Downloader to.
        :type state: str
        :raises NameError: Invalid state provided.
        """

        if state in self.__states:
            self.__state = state
        else:
            raise NameError("Invalid state")

    def get_state(self):
        """Returns the current state of the Downloader.

        :return: The state of the downloader.
        :rtype: str
        """

        return self.__state

    def start_stream(self):
        """Starts the downloader.
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
        """Returns the current list of videos being downloaded.

        :return: List of URLs being downloaded.
        :rtype: list
        """

        return self.__urlStream

    def run(self):
        """Starts downloading videos from the URL stream.
        Also prompts the user to install FFmpeg if there is no
        FFmpeg installation detected.
        """

        # Prompt the user to install FFmpeg (assuming they're on windows).
        if not ffmpegExists():
            print(textwrap.dedent("""\
            No FFmpeg installation detected. If you gave a format
            for videos to be converted to, they will not be converted.\n"""))
            if sys.platform == "win32":
                install_ffmpeg = input("No FFmpeg installation detected. Install? (Y/N)")

                if install_ffmpeg.lower() == "y":
                    setup()

        # Once stopped, the downloader will be "dead."
        while self.get_state() != "Stopped":

            # If it's unpaused, it wont do anything until it's unpaused.
            if self.get_state() == "Playing":
                convEnabled = self.__conversionParams.get("enabled")

                # Start downloading the newest video
                if len(self.__urlStream) > 0:
                    video = YouTube(self.__urlStream[0])
                    # Check if we're converting something to another format, download a low-res
                    # version so it takes less time to convert.

                    videoStream = video.streams.first() if not convEnabled else video.streams.get_lowest_resolution()
                    videoTitle = video.player_response["videoDetails"]["title"]
                    videoPath = videoStream.download(output_path=self.outputFolder, filename=videoTitle)

                    if self.__conversionParams.get("enabled") and ffmpegExists():
                        self.__convert(videoPath)

                    print(f"Downloaded video {videoTitle}")
                    self.__urlStream.pop(0)
                else:
                    if self.killAfterFinished:
                        self.stop_stream()
                    else:
                        self.pause_stream()
        else:
            self.set_state("Dead")

    def config_conversion(self, enabled=False, convertTo="mp3"):
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
