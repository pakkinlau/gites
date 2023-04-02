import util
import os

# Use this when choosing "All programming projects" as root folder.
os.chdir(r"D:\All_programming_projects")

list_of_repo = [
    "Early old works",
    "Git management",
    "Guides",
    "Python coding gym",
    "Textual notes",
    "Tutorial template",
    "Video materials",
    "JS webpage coding gym"
]

list_of_location = [f".\{elt}" for elt in list_of_repo]

# Initialize Git LFS for the repository.
os.system("git lfs install")

for elt in list_of_location:
    # Track large files with Git LFS.
    os.system(f"cd {elt} && git lfs track '*.zip' ' *.tar.gz' '*.mp4' '*.pdf'")
    # Check if any files added to the commit are larger than 100MB.
    files = os.popen(f"cd {elt} && git diff --cached --name-only --diff-filter=ACM").read().splitlines()
    for file in files:
        if os.path.getsize(os.path.join(elt, file)) > 100 * 1024 * 1024:
            print(f"{file} is larger than 100MB. Aborting push.")
            exit(1)
    # Push changes to GitHub.
    util.push(elt)