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
import validators
import argparse
from pytube import YouTube, Playlist

urlsToPass = []

# Add all the arguments (optional, or otherwise)
argParser = argparse.ArgumentParser(description="A script to download Youtube videos.",
                                    formatter_class=argparse.RawTextHelpFormatter)
argParser.add_argument("source", help="The place to extract URLs from. More info the README.md")
argParser.add_argument("-d", help="Whether or not debugging should happen.", action="store_true")
argParser.add_argument("-f", help="The format to convert the videos to.")
argParser.add_argument("-k", help="Whether or not to keep the downloaded video after conversion.",
                       action="store_true")

parsedArgs = argParser.parse_args()

# Setup all the URLs to pass to the Downloader.
sourceURL = parsedArgs.source

# If the URL is actually a valid URL
if validators.url(sourceURL):
    # If the URL is linking to a video or playlist.
    if sourceURL.startswith("https://www.youtube.com/watch?v="):
        urlsToPass.append(sourceURL)
    elif sourceURL.startswith("https://www.youtube.com/playlist?list="):
        urlsToPass = Playlist(sourceURL).video_urls

vDownloader = funcs.Downloader(".", urls=urlsToPass, logging=getattr(parsedArgs, "d"),
                               killAfterFinished=True, keepFile=parsedArgs.k)
vDownloader.start_stream()

# Configure the Downloader's conversion (if it's specified)
convertTo = getattr(parsedArgs, "f")

if convertTo:
    vDownloader.config_conversion(True, convertTo=convertTo)

# Start downloading & converting the videos.
vDownloader.run()
