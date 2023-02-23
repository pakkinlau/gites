import util
import os

# Use this when choosing "All programming projects" as root folder.
os.chdir(r"C:\Users\kinla\All_programming_projects")

list_of_repo = [
    "Early old works",
    "Git management",
    "Guides",
    "Python coding gym",
    "Textual notes",
    "Tutorial template",
    "Video materials",
]



list_of_location = [f".\{elt}" for elt in list_of_repo]

# Initialize Git LFS for the repository.
os.system("git lfs install")

for elt in list_of_location:
    # Track large files with Git LFS.
    os.system(f"cd {elt} && git lfs track '*.zip' + ' *.tar.gz' + ' *.mp4' + ' *.pdf'")
    # Push changes to GitHub.
    util.push(elt)