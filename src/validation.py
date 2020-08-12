# validation.py
# created by: spaceraiders
# contact: spaceraiders@protonmail.com
# description:  Includes functions used for validation of URLs that're
# used by download.py to verify if the commandline argument "Source" is
# a valid URL. If it isn't, it will attempt to "build" the URL, and switch
# it up with something else. Example:
# www.youtube.com is replaced with: https://www.youtube.com

import validators
from pathlib import Path
from pytube import Playlist

BUILDABLE_URLS = {
    "www.youtube.com": "https://",
    "youtube.com": "https://www."
}


def build_url(url):
    """Takes in a URL and tries to connect it with a
    segment of a completed URL. This is so you can put
    in www.youtube.com, which is incomplete, and come out
    with https://www.youtube.com, which is a valid URL.

    :param url: The URL to build from.
    :type url: str
    :return: The completed URL.
    :rtype: string
    """

    for buildable_url, append in BUILDABLE_URLS.items():
        if url.startswith(buildable_url):
            return append + url
    return url


def is_url(url):
    """Verifies that the given URL is a valid URL that can be
    used by PyTube. It will attempt to build a complete URL if
    the provided one is incomplete.

    :param url: The URL to check.
    :type url: str
    :return: Whether or not it is a valid URL.
    :rtype: bool
    """

    builtUrl = build_url(url)
    return bool(validators.url(builtUrl)), builtUrl


def is_playlist(url):
    """Verifies whether or not the provided URL is a Youtube
    Playlist. This is achieved by checking if the URL has a
    prefix unique to Playlists in the URL.

    :param url: The URL to verify.
    :type url: str
    :return: Whether or not the given URL links to a Playlist.
    :rtype: bool
    """

    isValidURL, url = is_url(url)

    return isValidURL and url.startswith("https://www.youtube.com/playlist?list=")


def is_video(url):
    """Verifies whether or not the provided URL is a Youtube
    Video. This is achieved by checking if the URL has a prefix
    unique to Videos in the URL.

    :param url: The URL to verify.
    :type url: str
    :return: Whether or not the given URL links to a Video.
    :rtype: bool
    """

    isValidURL, url = is_url(url)

    return isValidURL and url.startswith("https://www.youtube.com/watch?v=")


def is_file(path):
    """Verifies whether or not the provided path both exists,
    and is a text file, and not a directory or other filesystem
    structure. Turns string paths into Path-Like objects from
    pathlib.

    :param path: The path to the file.
    :type path: Path-like, str
    :return: Whether or not the path exists, and is a file.
    :rtype: bool
    """

    path = Path(path) if isinstance(path, str) else path

    return path.exists() and path.is_file()


def verify(url):
    """Goes through the process of verifying the given URL
    and loads the URL into a list of URLs based off the given
    input.

    :param url: The URL (or path) of the URL.
    :type url: Path-Like, str
    :return: The list of URLs for the Downloader to use.
    :rtype: list
    """

    url_storage = []

    # Build up the list containing all the URLs.
    if is_playlist(url):
        url_storage = Playlist(url).video_urls
    elif is_video(url):
        url_storage.append(url)
    elif is_file(Path(url)):
        # Load up URLs from a file, and verify that they're valid.
        with open(Path(url), "r") as urlFile:
            url_list = urlFile.readlines()

            for url_line in url_list:
                if is_url(url_line)[0]:
                    url_storage.append(url_line)

    return url_storage

