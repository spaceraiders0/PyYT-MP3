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

# Installation
There are a few ways of setting this up, since it doesn't necessarily work out of the box.
On it's own, this script can download videos, with PyTube, but that's about it. If you'd wish
to *convert* the resulting videos to an MP3, or other audio format, you're going to need to
install FFmpeg. <br>

### Windows
This script was originally, mostly created on Windows, so I implemented functionality to install
FFmpeg for you, but only to the project's directory. That is, if there isn't already an FFmpeg
installation detected. This is exclusive to Windows, however. If you'd like to have it be usable
globally across windows, you can use manually download, and add FFmpeg to your path from this URL:
https://www.ffmpeg.org

### Linux
If you're on Linux, you're out of luck on getting FFmpeg automatically installed by this script.
This is mostly because you can easily install it by using your package manager.

Ubuntu, it's related flavors, or any distro using APT:
```
sudo apt-get install ffmpeg
```

### Mac
Unfortunately, I do not own a Mac, so I couldn't exactly test this on the OS. For all I know, this
could function completely normally on a Mac. In the case you are running a Mac, you should assume
that this script is broken. If you'd like, however, you can test it and let me know how it functions.

# Notices
As of this time, I used the specific GitHub repository to install PyTube instead of the one downloaded
directly from pip. It appears to be more stable, so I suggest you to do the same. That being said, however,
PyTube currently has a lot of errors that have not been fixed in any sort of stable build. Here are some common
ones you may come across, and Issue pages on how to get them fixed.

If you'd like to download the specific GitHub repository because the one from PyPi doesn't work, run this command:
pip3 install git+https://github.com/spaceraiders0/PyYT-MP3

### Keyword Error 'cipher'
https://github.com/nficano/pytube/issues/642

# Credits
PyTube, by nficano https://github.com/nficano/pytube <br/>
FFmpeg, by the FFmpeg Team: https://www.ffmpeg.org
