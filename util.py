import subprocess
import os

from datetime import datetime

now = datetime.now()

list_of_repo = [
    "Early old works",
    "Git management",
]

list_of_location = [f".\{elt}" for elt in list_of_repo]


def push(folder_location, tag_message=""):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # 16/09/2022 22:29:34

    """ Change your file location here """
    # os.chdir(folder_location.encode("unicode_escape"))
    subprocess.run("git status", shell=True, cwd=folder_location)
    subprocess.run("git add --all", shell=True, cwd=folder_location)

    """ Change your upload tag here"""
    subprocess.run(
        f'git commit -m"{dt_string}, {tag_message}"', shell=True, cwd=folder_location
    )
    subprocess.run(f"git push origin main", shell=True, cwd=folder_location)

    print(f"Completed. Tag: {dt_string}")


for elt in list_of_location:
    push(elt)


def clean_undone_commit():
    """When crashes (eg: some large files included in the commit), clean undone commit by this."""
    subprocess.run(f"git reset --soft HEAD~", shell=True)


def check_ignored_path():
    """Before this, make sure .gitignore file is located in the root directory of the repository."""
    subprocess.run(f"git status --ignored", shell=True)
