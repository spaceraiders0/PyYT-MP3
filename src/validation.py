import validators
from pathlib import Path
from pytube import YouTube, Playlist

BUILDABLE_URLS = {
    "www.youtube.com": "https://",
    "youtube.com": "https://www."
}

def build_url(url):
    for buildable_url, append in BUILDABLE_URLS.items():
        if url.startswith(buildable_url):
            return append + url     
    return url
        
def is_url(url):
    builtUrl = build_url(url)
    return bool(validators.url(builtUrl)), builtUrl

def is_playlist(url):
    isValidURL, url = is_url(url)

    return isValidURL and url.startswith("https://www.youtube.com/playlist?list=")
    
def is_video(url):
    isValidURL, url = is_url(url)
    
    return isValidURL and url.startswith("https://www.youtube.com/watch?v=")


def is_file(path):
    return path.exists() and path.is_file()

def verify(url, urlStorage):
    if is_playlist(url):
        urlStorage.append(Playlist(url).video_urls)
    elif is_video(url):
        urlStorage.append(YouTube(is_video))
    elif is_file(Path(url)):
        with open(Path(url), "r") as urlFile:
            url_list = urlFile.readlines()

            for url_line in url_list:
                print(url_line)
    
