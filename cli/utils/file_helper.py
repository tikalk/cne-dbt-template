import os
from typing import List

from cli.const.constant import FileNames


def get_root_dir():
    if os.path.exists(FileNames.DBT_PROJECT_FILE):
        return os.getcwd()
    else:
        raise Exception("Running from an unknown directory")


def get_target_dir():
    return os.path.join(get_root_dir(), "target")


def get_models_dir():
    models = os.path.join(get_root_dir(), "models")
    # if not os.path.exists(models):
    #     os.makedirs(models)
    return models


def get_macros_dir():
    return os.path.join(get_root_dir(), "macros")


def get_resources_dir():
    return os.path.join(get_root_dir(), "cli", "resources")


def get_templates_dir():
    return os.path.join(get_resources_dir(), "templates")


def get_folder_names(root_dir: str = ".") -> List[str]:
    """
    Get a list of all folders (directories) under the specified root directory.

    Args:
        root_dir (str): The root directory to start searching from. Defaults to current directory.

    Returns:
        List[str]: List of name to all folders found
    """
    return [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]


def get_folder_content(root_dir: str = ".") -> List[str]:
    return [f for f in os.listdir(root_dir)]


def list_files(directory, extension=None):
    """
    Lists all files in a given directory with an optional extension filter.

    :param directory: Path to the directory.
    :param extension: File extension to filter by (e.g., '.txt'). If None, lists all files.
    :return: List of matching file paths.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Invalid directory: {directory}")

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and (extension is None or f.endswith(extension))]

    return files
