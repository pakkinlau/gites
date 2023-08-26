# importing other modules: 
from .subpackage.CreateRepoManager import initialize_repo
from .subpackage.GitPushManager import bulkpush
from .subpackage.JSONUpdater import load_data, update_root_into, update_repo_info
from .subpackage.RepoCloner import bulkclone

from .subpackage.util import *

from .subpackage.ConfigJSONHandler import DatastoreLocationChecker



import argparse


def entry():
    """This function returns the determined datastore json path if it is set. 
    Help the user config it if it is the first time"""
    datastore_path = DatastoreLocationChecker().load_setup_json_and_get_datastore_json_address()
    return datastore_path

def synthesis_root_dir(folder_name):
    # from datastore path, get the root directory.
    # with the root directory and the Folder name, get the full path.

    pass

def bulkpush(args):
    # Implement your bulkpush functionality here
    print("Performing bulk push...")

def bulkpull(args):
    # Implement your bulkpull functionality here
    print("Performing bulk pull...")

def main_bulkpush():
    parser = argparse.ArgumentParser(description="My CLI Tool - Bulk Push")
    # Add arguments specific to bulkpush command if needed
    args = parser.parse_args()
    bulkpush(args)

def main_bulkpull():
    parser = argparse.ArgumentParser(description="My CLI Tool - Bulk Pull")
    # Add arguments specific to bulkpull command if needed
    args = parser.parse_args()
    bulkpull(args)

if __name__ == "__main__":
    main_bulkpush()