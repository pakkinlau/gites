"""
This cli.py is just an interface that collect and manage all the actions,
which help centralize the logic for handling variaous commands and make it easier to maintain 
and expand in the future. 

There are two parts need to be edited to make CLI works. 
1. cli.py: it is an adapter between CLI listener in `setup.py` and the functionalities from subpackages,
2. setup.py: the `entry_points` attribute setup the listeners and the related keywords, that subsequently
the user can use them in their terminal to trigger those functionalities. 
"""

# importing other modules: 
from .subpackage.CreateRepoManager import initialize_repo
from .subpackage.GitPushManager import GitPushManager
from .subpackage.RepoCloner import bulkclone

from .subpackage.util import *

from .subpackage.ConfigJSONHandler import ConfigJSONHandler
from .subpackage.DatastoreJSONHandler import DatastoreJSONHandler


import argparse

def _check_datastore_location():
    """This function would be optionally used by multiple CLI actions. """
    datastore_json_path = ConfigJSONHandler.check_initial_setup_then_get_datastore_json_address()

def lpush():
    root_dir = DatastoreJSONHandler.root_dir
    GitPushManager.lpush()

def main():
    parser = argparse.ArgumentParser(description='Command-line interface for gites package')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create a subparser for the 'push' command
    push_parser = subparsers.add_parser('push', help='Push changes to Git')
    push_parser.set_defaults(func=GitPushManager.lpush)

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