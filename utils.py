import os
import shutil

def clear_folder(path):
    """
    Deletes a folder, then create it again.
    """
    # deletetion
    try:
        shutil.rmtree(path)
        print(f"Folder {path} was successfully deleted")
    except OSError as e:
        print(f"Could not delete folder {path}: {e}")
    # creation
    os.makedirs(path)