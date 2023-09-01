"""
This cli.py is just an interface that collect and manage all the actions,
which help centralize the logic for handling variaous commands and make it easier to maintain 
and expand in the future. 

There are two parts need to be edited to make CLI works. 
1. cli.py: it is an adapter between CLI listener in `setup.py` and the functionalities from subpackages,
2. setup.py: the `entry_points` attribute setup the listeners and the related keywords, that subsequently
the user can use them in their terminal to trigger those functionalities. 
"""


from subpackage.ConfigJSONHandler import ConfigJSONHandler
from subpackage.GitPushManager import GitPushManager

import argparse

def _check_datastore_location():
    """This function would be optionally used by multiple CLI actions. """
    datastore_json_path = ConfigJSONHandler.check_initial_setup_then_get_datastore_json_address()

def cli_lpush():
    parser = argparse.ArgumentParser(description='Push changes to Git')
    args = parser.parse_args()
    GitPushManager().lpush() 

def main():
    parser = argparse.ArgumentParser(description='Command-line interface for gites package')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create a subparser for the 'push' command
    push_parser = subparsers.add_parser('push', help='Push changes to Git')
    push_parser.set_defaults(func=cli_lpush)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func()

if __name__ == "__main__":
    cli_lpush()