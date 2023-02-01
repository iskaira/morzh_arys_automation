# import OS module
import os
from typing import List

from app.config import FilesDirectory


MAX_MESSAGE_LENGTH = 4096


# Get the list of all files and directories
def get_dirs_list() -> List[str]:
    return os.listdir(FilesDirectory)


def get_files_list(directory: str) -> List[str]:
    directory = f"{FilesDirectory}//{directory}"
    return os.listdir(directory)


def smart_split(text: str, chars_per_string: int = MAX_MESSAGE_LENGTH) -> List[str]:
    def _text_before_last(substr: str) -> str:
        return substr.join(part.split(substr)[:-1]) + substr

    if chars_per_string > MAX_MESSAGE_LENGTH:
        chars_per_string = MAX_MESSAGE_LENGTH
    parts = []
    while True:
        if len(text) < chars_per_string:
            parts.append(text)
            return parts
        part = text[:chars_per_string]
        if "\n" in part:
            part = _text_before_last("\n")
        elif ". " in part:
            part = _text_before_last(". ")
        elif " " in part:
            part = _text_before_last(" ")
        parts.append(part)
        text = text[len(part):]
