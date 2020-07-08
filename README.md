# PyYT-MP3
PyYT-MP3 is a script I wrote that acts as a wrapper around the Python module PyTube. It takes an Object Oriented
approach to handling the downloading of videos by allowing the use of individual "Downloader objects." These can be
given individual sets of URLs to be converted to their own individual file formats using FFmpeg.

# Motivations
There were a few reasons behind the making of this script. Mostly for my own purposes, but someone else might find
this useful at some point.
- Long video times are often not allowed by YouTube conversion sites
- It must be done through a website, which is often both closed source, and may contain suspicious components.
- Bulk conversion, as well as playlists, while possible through specific websites, are almost never accessible
in the same place.
- I wanted to try my hand at making a wrapper.

# Credits
PyTube, by nficano https://github.com/nficano/pytube <br/>
FFmpeg, by the FFmpeg Team: https://www.ffmpeg.org