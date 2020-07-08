# PyYT-MP3

# Description
A little script I wrote that acts as a wrapper around acommand-line
utility called PyTube. It can take input from many sources, including
Playlists, text file(s), and direct video URLs, and optionally convert
them to MP3, or keep them as an MP4.

# Motivation
This script is my magnum opus. My response to those shady Youtube > MP3 websites. No longer must suspicious websites be used. No longer must there be limited video download lengths.

# How To Use
While the -h argument when calling main.py is intended for actually providing help on how to use the
other argument, It is difficult to fit each description on one line, and I can't include examples, so
I will use this.
<br/>
As of writing this, these are the only arguments you can give the script
<br/>
Positional Arguments<br/>
&nbsp;source: This argument will specify where the script will grab links from.
&nbsp;As stated in the description, this script can take in multiple forms of
&nbsp;input for the source argument. This includes<br/>
&nbsp;&nbsp;- Playlists (python main.py PLAYLIST_URL)<br/>
&nbsp;&nbsp;- Direct video link (python main.py VIDEO_URL)<br/>
&nbsp;&nbsp;- A text file (python main.py PATH_TO_TEXT_FILE)<br/>
&nbsp;&nbsp;- A directory (python main.py PATH_TO_DIRECTORY)<br/>
<br/>
&nbsp;I feel the only input type that may need explaining is the directory. All
&nbsp;it does, is search through the directory (recursively, mind you), for text
&nbsp;files containing URLs. While this may be a niche use-case, I felt it would
&nbsp;be a nice option to have.<br/>
<br/>
Optional Arguments<br/>
&nbsp;--output This argument tells the script where you want the output to be
&nbsp;dumped to. In the script itself, this defaults to the data folder's output
&nbsp;directory, which is created when the script is ran.
<br/>
&nbsp;HOW TO USE<br/>
&nbsp;&nbsp;python main.py SOURCE --output PATH/TO/DIRECTORY<br/>
<br/>
&nbsp;--to-mp3 This flag tells the script that you want to convert all videos
&nbsp;downloaded to MP3. If this flag is not specified, they will simply be kept
&nbsp;as MP4's.
<br/>
&nbsp;HOW TO USE<br/>
&nbsp;&nbsp;python main.py SOURCE --to-mp3<br/>
<br/>
# Notices
Currently, as of release v9.6.0 of PyTube, there exists a bug where downloaded videos
will have the name "YouTube". To combat this, and prevent file conflictions, when the
video is downloaded, a check is performed on files with the name YouTube. If they are
named this, they will be named based off the system time. I will be removing this check
once the bug is finally fixed.
<br/>
Through testing, I have discovered that *shortened YouTube URLs* will not work when they
are put through the script. Keep this in mind.
<br/>
# Credits
PyTube, by nficano https://github.com/nficano/pytube<br/>
FFmpeg, by the FFmpeg Team: https://ffmpeg.org/<br/>