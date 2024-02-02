import os

from utils import flatten

def list_files_in_directory(dirname: str):
    """
    Lists the files in a directory as their name including the provided dirname, 
    can be either directories or files

    Args:
        dirname (str): The path to the directory to list files in, 
        relative to the execution dir of this script
    
    Returns:
        list: List containing file names
    """
    return [f"{dirname}/{file}" for file in os.listdir(dirname)]

def walk_directory_tree(dirname: str):
    """
    Traverses the directory tree, starting in the provided directory
    and fetches all files it finds, returning them as a list containing
    their full path relative to the start dir.

    Args:
        filepath (str): where to start the traversal

    Returns:
        list: Containing each files it encounters during the traversal
    """
    if os.path.isfile(dirname):
        return dirname
    
    nested_filenames = [walk_directory_tree(f"{file_name}") for file_name in list_files_in_directory(dirname)]
    return flatten(nested_filenames)

def extract_audio_files(files, valid_extensions = ["wav", "aiff"]):
    """
    Accepts a list of files and returns a new list, containing only the files that 
    corresponds to an audio file type

    Args:
        files (list): The files to filter
        valid_types (list): (Optional) the supported audio file types
    
    Returns:
        list: A new list containing only the files of the desired type
    """
    def is_audio_file(file):
        return file.split(".")[-1] in valid_extensions

    return list(filter(is_audio_file, files))

def create_dir_for_file(file: str):
    """
    Accepts a file name including a file path and makes sure that the path up to the file name exists

    Args:
        file (str): The file to create directory structure for
    """
    parts = file.split("/")[:-1]
    path = "/".join(parts)
    if not os.path.exists(path):
        os.makedirs(path)

def convert_filename_to_mp3(filename: str):
    """
    Expects a file name and replaces the extension with .mp3

    Args:
        filename (str): the file to update extension for
    
    Returns:
        str: The same file name but extension replaced with .mp3
    """
    return f"{'.'.join(filename.split('.')[0:-1])}.mp3"
