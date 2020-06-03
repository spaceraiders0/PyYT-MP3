# PyYT-MP3

# Description
A little script I wrote that acts as a wrapper around acommand-line
utility called PyTube. It can take input from many sources, including
Playlists, text file(s), and direct video URLs, and optionally convert
them to MP3, or keep them as an MP4.

# How To Use
While the -h argument when calling main.py is intended for actually
providing help on how to use the other argument, It is difficult to
fit each description on one line, and I can't include examples, so I will
use this.
  
As of writing this, these are the only arguments you can give the script:
  
Positional Arguments:  
	source: This argument will specify where the script will grab links from.
	As stated in the description, this script can take in multiple forms of
	input for the source argument. This includes:  
		- Playlists (python main.py PLAYLIST_URL)  
		- Direct video link (python main.py VIDEO_URL)  
		- A text file (python main.py PATH_TO_TEXT_FILE)  
		- A directory (python main.py PATH_TO_DIRECTORY)  

	I feel the only input type that may need explaining is the directory. All
	it does, is search through the directory (recursively, mind you), for text
	files containing URLs. While this may be a niche use-case, I felt it would
	be a nice option to have.  

Optional Arguments:  

# Credits
PyTube, by nficano: https://github.com/nficano/pytube  
FFmpeg, by the FFmpeg Team: https://ffmpeg.org/  