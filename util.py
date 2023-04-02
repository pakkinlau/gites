import subprocess
import os

from datetime import datetime

now = datetime.now()


def push(folder_location, tag_message=""):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # 16/09/2022 22:29:34

    """ Change your file location here """
    # os.chdir(folder_location.encode("unicode_escape"))
    subprocess.run("git status", shell=True, cwd=folder_location)
    
    
    #""" Check whether it is running in main branch"""
    #subprocess.run("git branch main")
    #subprocess.run("git checkout main")
    

    """ Change your upload tag here"""
    subprocess.run("git add --all", shell=True, cwd=folder_location)
    subprocess.run(
        f'git commit -m"{dt_string}, {tag_message}"', shell=True, cwd=folder_location
    )
    subprocess.run(
        f"git push origin main", shell=True, cwd=folder_location, stdout=subprocess.PIPE
    )
    # Catch the output and detect if any error exist, stop the loop.
    print(f"Completed. Tag: {dt_string}")


def clean_undone_commit():
    """When crashes (eg: some large files included in the commit), clean undone commit by this."""
    subprocess.run(f"git reset --soft HEAD~", shell=True)


def check_ignored_path():
    """Before this, make sure .gitignore file is located in the root directory of the repository."""
    subprocess.run(f"git status --ignored", shell=True)
