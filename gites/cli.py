"""
This cli.py is just an interface that collect and manage all the actions,
which help centralize the logic for handling variaous commands and make it easier to maintain 
and expand in the future. 

There are two parts need to be edited to make CLI works. 
1. cli.py: it is an adapter between CLI listener in `setup.py` and the functionalities from subpackages.
argparse module parse 'subcommands' from command-line arguments. 


2. setup.py: the `entry_points` attribute setup the listeners and the related keywords.
'gites' considered as entry-point and the first keyword of the command to invoke the package.
"""


from .subpackage.config_json_handler import ConfigJSONHandler
from .subpackage.git_push_manager import GitPushManager
from .subpackage.repo_cloner import RepoCloner
from .subpackage.pull_manager import GitPullManager

import argparse

def _check_datastore_location():
    """This function would be optionally used by multiple CLI actions. """
    datastore_json_path = ConfigJSONHandler.check_initial_setup_then_get_datastore_json_address()

def cli_lpush():
    GitPushManager().lpush() 

def cli_lclone():
    RepoCloner().lclone() 

def cli_lpull():
    GitPullManager().lpull() 

def main():
    parser = argparse.ArgumentParser(description='Command-line interface for gites package')
    # subparsers handle subcommands. 
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create a subparser for the 'push' command
    push_parser = subparsers.add_parser('lpush', help='Push changes to Git')
    push_parser.set_defaults(func=cli_lpush)

    clone_parser = subparsers.add_parser('lclone', help='Clone a list of repos from Git to local computer')
    clone_parser.set_defaults(func=cli_lclone)

    pull_parser = subparsers.add_parser('lpull', help='Pull a list of repos of local computer')
    pull_parser.set_defaults(func=cli_lpull)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func()

"""
Also check the CLI entry point script at <package_root_folder>/bin/gites.
There should be a shebang in the first line, to be something like: #!/usr/bin/env python
"""

# The content of that file would be like:
"""
#!/home/kin/anaconda3/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from gites.cli import cli_lpush
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(cli_lpush())
"""


if __name__ == "__main__":
    cli_lpush()

