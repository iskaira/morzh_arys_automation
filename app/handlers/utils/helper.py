# import OS module
import os
from typing import List

from app.config import FilesDirectory


# Get the list of all files and directories
def get_dirs_list() -> List[str]:
    dirs = os.listdir(FilesDirectory)
    dirs.sort(reverse=True)
    return dirs


def get_files_list(directory: str) -> List[str]:
    directory = f"{FilesDirectory}//{directory}"
    files = os.listdir(directory)
    files.sort()
    return files
