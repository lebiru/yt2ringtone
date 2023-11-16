
import sys
import codecs
from pytube import YouTube
from moviepy.editor import *
import os
import re

# Set default encoding to UTF-8
if sys.version_info[0] == 3:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def sanitize_filename(filename):
    """Remove or replace special characters in the filename."""
    return re.sub(r'[^a-zA-Z0-9\-_\.]', '_', filename)

def download_video(url):
    """Download YouTube video."""
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.download()
    sanitized_filename = sanitize_filename(filename)
    os.rename(filename, sanitized_filename)
    return sanitized_filename

def convert_to_m4r(filename):
    """Convert the audio file to m4a format and then rename to m4r."""
    try:
        clip = AudioFileClip(filename)
        m4a_filename = filename.replace('.mp4', '.m4a')
        clip.write_audiofile(m4a_filename, codec='aac')
        m4r_filename = m4a_filename.replace('.m4a', '.m4r')
        os.rename(m4a_filename, m4r_filename)
        return m4r_filename
    except UnicodeEncodeError:
        print("An encoding error occurred. Skipping this file.")
        return None

def youtube_to_m4r(url):
    """Download a YouTube video and convert it to m4r."""
    filename = download_video(url)
    if filename:
        m4r_filename = convert_to_m4r(filename)
        if m4r_filename:
            print(f"Ringtone saved as {m4r_filename}")

# Prompt the user for the YouTube URL
youtube_url = input("Enter the YouTube video URL: ")
youtube_to_m4r(youtube_url)
