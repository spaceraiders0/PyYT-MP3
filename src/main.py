# main.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: A small script to download Youtube videos.

from pytube import YouTube
from argparse import ArgumentParser
from pathlib import Path as toPath
import os
import funcs

urls = []
output = toPath("../data/output")
input_folder = toPath("../data/input")
ffmpeg = os.path.abspath(toPath("../ffmpeg/bin/ffmpeg.exe"))
parser = ArgumentParser()


def next_prog(max_num, scale):
    percent = round(scale/max_num*100)
    prog_char, none_char = "=", " "
    total_prog = f"<{prog_char * percent}{none_char * (100-percent)}>"
    print(total_prog, end="\r")


# Starts up the argument parser for cuztomized functionality
parser.add_argument("--from-input", help="""flag to take URLs from the input
                    folder.""", action="store_true")
parser.add_argument("--from-url", help="""flag to download from a URL.""")
parser.add_argument("--output", help="""specifies a custom directory to dump
                    output to""")
parser.add_argument("--input", help="""specifies a custom directory to extract
                    URls from. compliments --from-input""")

args = parser.parse_args()

# Assigns new folders to input, or output. Validates the path aswell.
if args.output:
    new_path = toPath(args.output)

    if os.path.exists(new_path):
        output = new_path
    else:
        print(f"Invalid output folder! You gave: {new_path}")

if args.input:
    new_path = toPath(args.input)

    if os.path.exists(new_path):
        input = new_path
    else:
        print(f"Invalid input folder! You gave {new_path}")

# This appends or collects all URLs from a source. EWither the stdin, or files.
if args.from_input:
    # This is RECURSIVE. It will go through ALL FOLDERS in the directory.

    # Extract URLs from text files
    for dirpath, _, filenames in os.walk(input_folder):
        for filename in filenames:
            file_to_open = toPath(dirpath + f"/{filename}")

            with open(file_to_open, "r") as url_container:
                extracted_urls = url_container.readlines()

                for url in extracted_urls:
                    urls.append(url.strip("\n"))
elif args.from_url:
    urls.append(args.from_url)

# Download the videos from the URL list, then conver them to an MP3
# Clean this up in the morning!
# Give different text files their own folders in output maybe?
# add playlists tomorrow too
# add Try statement for failed yt videos
# add option to convert to mp3, and whether or not to keep both the mp4 and mp3
# add a settings menu

#print("Downloading N/A", end="\r")
next_prog(len(urls), 0)

for url in urls:
    try:
        try:
            url_index = urls.index(url)
        except ValueError:
            pass
        yt_obj = YouTube(url)
       # print(f"Downloading {yt_obj.title}", end="\r\n")
        stream = yt_obj.streams.first()
        path_to_video = stream.download(output_path=output)
        root_path = os.path.abspath(os.path.splitext(path_to_video)[0])

        os.system(f"""{str(ffmpeg)} -i \"{root_path}.mp4\" \"{root_path}.mp3\" -loglevel warning""")
        next_prog(len(urls), url_index+1)
        os.remove(path_to_video)
    except KeyError:
        pass
