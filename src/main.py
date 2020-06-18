# main.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: A small script to download Youtube videos.

# TODO
# Document more of the functions in funcs.py
#
# Finish validating whether or not FFmpeg is installed on this machine.
# Maybe make it check if it's in the path?
#
# Instead of checking for FFmpeg's folder, check for the EXE.
#
# It would be cool to have this be put into the PATH of the machine it's
# being ran on, but support would be required for Linux too.
#
# Give different text files their own folders in output maybe?
#
# Consider an Object Oriented approach to the downloader.
#
# Autogenerate the folders data, data/input, and data/output. Git doesn't
#
# Make all directories be based off the file's tree, rather than
# which directory it was ran from.
#
# Implement a temporary folder for the FFmpeg installation and mp4's downloaded
# IF they're being converted to an mp3.
#
# Add check for when files have the same name when downloaded.

import os
import funcs
import requests
import time
import pytube.exceptions as pyt_excep
from pytube import YouTube, Playlist
from argparse import ArgumentParser
from pathlib import Path as toPath

urls = []
output = toPath("../data/output")
input_folder = toPath("../data/input")
ffmpeg = os.path.abspath(toPath("../ffmpeg/bin/ffmpeg.exe"))
parser = ArgumentParser()

# Starts up the argument parser for customized functionality
parser.add_argument("source", help="""specifies the source where videos are located.
                    further information on what input can be is located in the
                    README.""")
parser.add_argument("--output", help="""specifies a custom directory to dump
                    output to""")
parser.add_argument("--to-mp3", help="""specifies whether or not to convert output
                    to an MP3.""", action="store_true")

args = parser.parse_args()
funcs.setup()

if args.source:
    text_files = []
    source = args.source

    # check types for all valid inputs
    if os.path.isdir(source):
        # RECURSIVELY get all text files and append their paths to text_files
        for dirpath, _, filenames in os.walk(source):
            for filename in filenames:
                text_files.append(toPath(f"{dirpath}/{filename}"))

    # assuming it's a URL, validate it, and extract the url, or all the
    # videos in the provided playlist's.
    elif funcs.validate_url(source):
        try:
            extracted_urls = Playlist(source)
            urls = [*extracted_urls]
        except KeyError:
            urls.append(source)

    elif os.path.isfile(source):
        text_files.append(source)

    else:
        print("Invalid input.")

    # go through all defined text files and get their urls
    for textfile in text_files:
        with open(textfile, "r") as url_list:
            for url in url_list.readlines():
                funcs.validate_url(url, insertion=urls)

# Assigns new folders to input, or output. Validates the path as well.
if args.output:
    new_path = toPath(args.output)

    if os.path.exists(new_path):
        output = new_path
    else:
        print(f"Invalid output folder! You gave: {new_path}")

# Download and convert (if the flag is true) YouTube videos.
for index in range(0, len(urls)):
    try:
        url = urls[index]
        video = YouTube(url)
        video_name = video.title
        progress = str(round((index + 1) / len(urls) * 100)) + "% completed"
        video_downloading = f"Downloading video {video_name}"

        if video_name == "YouTube":
            video_name = str(round(time.time()))

        stream = video.streams.first()
        path_to_video = stream.download(output_path=output, filename=video_name)
        root_path = os.path.abspath(os.path.splitext(path_to_video)[0])

        # Check if the convert to MP3 flag is True.
        if args.to_mp3:
            os.system(f"""{str(ffmpeg)} -i \"{root_path}.mp4\" \"{root_path}.mp3\" -loglevel warning""")
            os.remove(path_to_video)

    except (KeyError, pyt_excep.RegexMatchError, pyt_excep.VideoUnavailable):
        print(f"Couldn't download video. ({url})")

    except pyt_excep.LiveStreamError:
        print("Cannot download livestream.")
