#!/usr/bin/python3

# main.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: A small script to download Youtube videos.

# TODO
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
# Test lower-quality MP4's to convert to MP3's in hopes of quicker
# conversion times.
#
# Make all directories be based off the file's tree, rather than
# which directory it was ran from.
#
# Implement a temporary folder for the FFmpeg installation and mp4's downloaded
# IF they're being converted to an mp3.
#
# Add a "logger" argument to main.py, --logger
#
# Cause the FFmpeg folder to be deleted on KeyboardInterrupt to prevent
# conflictions. 
#
# Add check for when files have the same name when downloaded.

import pathlib
import funcs
from argparse import ArgumentParser

urlsToPass = []

# Add all the arguments (optional, or otherwise)
argParser = ArgumentParser(description="A script to download Youtube videos.")
argParser.add_argument("source", help="The place to extract URLs from. More info the README.md")
argParser.add_argument("--debug", help="Whether or not debugging should happen.",
                        action="store_true")

parsedArgs = argParser.parse_args()
vDownloader = funcs.Downloader(".", logging=hasattr(parsedArgs, "debug"))


