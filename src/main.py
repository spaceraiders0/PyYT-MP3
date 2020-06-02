# main.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: A small script to download Youtube videos.

# TODO
# > Document more of the functions in funcs.py
# > Finish validating whether or not FFmpeg is installed on this machine.
# Maybe make it check if it's in the path?
# > It would be cool to have this be put into the PATH of the machine it's
# being ran on, but support would be required for Linux too.

from pytube import YouTube, Playlist
from argparse import ArgumentParser
from pathlib import Path as toPath
import os, funcs, validators

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

args = parser.parse_args()

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
        print("Parsing URL.")
        try:
            extracted_urls = Playlist(source)
            urls = [*extracted_urls]
        except KeyError:
            YouTube(source)
            urls = [source]

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


# Download the videos from the URL list, then convert them to an MP3
# Clean this up in the morning!
# Give different text files their own folders in output maybe?
# add playlists tomorrow too
# add Try statement for failed yt videos
# add option to convert to mp3, and whether or not to keep both the mp4 and mp3
# add a settings menu

# print("Downloading N/A", end="\r")
#next_prog(len(urls), 0)

for url in urls:
    try:
        yt_obj = YouTube(url)
        stream = yt_obj.streams.first()
        path_to_video = stream.download(output_path=output)
        root_path = os.path.abspath(os.path.splitext(path_to_video)[0])
        print(root_path)

        os.system(f"""{str(ffmpeg)} -i \"{root_path}.mp4\" \"{root_path}.mp3\" -loglevel        warning""")

        os.remove(path_to_video)
    except KeyError:
        pass
