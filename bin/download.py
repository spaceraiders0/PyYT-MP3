#!/usr/bin/python

# main.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: A small script to download Youtube videos.

import sys
import argparse
from pathlib import Path
from threading import Thread
from validation import verify

# Add the src directory. If you have a cleaner method of doing this, please edit it.
sys.path.append(str(Path(__file__).parent.absolute().parent / Path("src")))

from downloader import Downloader, ffmpegExists, setup, live


# Add all the arguments (optional, or otherwise)
argParser = argparse.ArgumentParser(description="A script to download Youtube videos.")
argParser.add_argument("source", help="The place to extract URLs from. More info the README.md", nargs="*")
argParser.add_argument("-f", help="The format to convert the videos to.")
argParser.add_argument("-l", help="Whether or not to start the script in Live mode.", action="store_true")
argParser.add_argument("-s", help="Flag to setup FFmpeg.", action="store_true")
argParser.add_argument("-o", help="The output directory. Defaults to the Current Working Directory.",
                       default=".")
argParser.add_argument("-k", help="Whether or not to keep the downloaded video after conversion.",
                       action="store_true")

parsedArgs = argParser.parse_args()

# Install FFmpeg if the argument is present.
if parsedArgs.s and not ffmpegExists():
    print("Setting up FFmpeg.\n")
    setup()
elif parsedArgs.s and ffmpegExists():
    print("FFmpeg already installed.\n")

# Load up all the URLs and verify sources.
urlsToPass = verify(parsedArgs.source)
vDownloader = Downloader(parsedArgs.o, urls=urlsToPass, killAfterFinished=not parsedArgs.l, keepFile=parsedArgs.k,
                         silent=parsedArgs.l)
vDownloader.start_stream()

# Configure the Downloader's conversion (if it's specified)
convertTo = getattr(parsedArgs, "f")

if convertTo:
    vDownloader.config_conversion(True, convertTo=convertTo)

# Live mode
if parsedArgs.l:
    Thread(target=live, args=(vDownloader,)).start()

# Start downloading & converting the videos.
vDownloader.run()
