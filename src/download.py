#!/usr/bin/python3

# main.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description: A small script to download Youtube videos.

import pathlib
import validators
import argparse
from downloader import Downloader
from validation import verify

urlsToPass = []

# Add all the arguments (optional, or otherwise)
argParser = argparse.ArgumentParser(description="A script to download Youtube videos.")
argParser.add_argument("source", help="The place to extract URLs from. More info the README.md")
argParser.add_argument("-d", help="Whether or not debugging should happen.", action="store_true")
argParser.add_argument("-f", help="The format to convert the videos to.")
argParser.add_argument("-k", help="Whether or not to keep the downloaded video after conversion.",
                       action="store_true")

parsedArgs = argParser.parse_args()

# Setup all the URLs to pass to the Downloader.
sourceURL = parsedArgs.source

# Load up all the URLs and verify sources. 
verify(parsedArgs.source, urlsToPass)
print(urlsToPass)

vDownloader = Downloader(".", urls=urlsToPass, logging=getattr(parsedArgs, "d"),
                         killAfterFinished=True, keepFile=parsedArgs.k)

vDownloader.start_stream()

# Configure the Downloader's conversion (if it's specified)
convertTo = getattr(parsedArgs, "f")

if convertTo:
    vDownloader.config_conversion(True, convertTo=convertTo)

# Start downloading & converting the videos.
vDownloader.run()