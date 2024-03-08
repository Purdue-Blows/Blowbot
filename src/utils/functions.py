import re
from discord.ext import commands


def escape_special_characters(file_name):
    # Define a regular expression pattern to match special characters
    special_characters = r'[\\/:\*\?"<>\| ]'

    # Replace special characters with an underscore
    safe_file_name = re.sub(special_characters, "_", file_name)
    print("Safe file name is: ")
    print(safe_file_name)
    return safe_file_name


def to_mp3_file(ext):
    ext = ext.replace("webm", "mp3")
    ext = ext.replace("mp4", "mp3")
    ext = ext.replace(".mov", ".mp3")
    return ext
