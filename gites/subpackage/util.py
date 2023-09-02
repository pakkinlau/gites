"""
The followings are legacy functions. No application for now. 
"""

import os
import subprocess
import shutil



# This should be used in more than 1 module.... Check it. 
def check_and_copy_pre_commit_hook(repo_location):
    hooks_dir = os.path.join(repo_location, ".git", "hooks")
    pre_commit_hook_path = os.path.join(hooks_dir, "pre-commit")
    pre_made_hook_path = os.path.join(os.path.dirname(__file__), "My hooks", "pre-commit")  # Replace this with the actual path of your pre-made hook.

    if not os.path.exists(hooks_dir):
        os.makedirs(hooks_dir)

    if not os.path.exists(pre_commit_hook_path):
        print("Copying pre-commit hook...")
        shutil.copy(pre_made_hook_path, pre_commit_hook_path)
        os.chmod(pre_commit_hook_path, 0o755)
        print("Pre-commit hook copied.")
    else:
        print("Pre-commit hook already exists.")

def get_files_bigger_than_100mb(folder_path):
    file_list = []

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to megabytes

            if file_size_mb > 100:
                file_list.append(os.path.relpath(file_path, start=folder_path))

    return file_list

def clean_undone_commit():
    """When crashes (eg: some large files included in the commit), clean undone commit by this."""
    subprocess.run(f"git reset --soft HEAD~", shell=True)


def check_ignored_path():
    """Before this, make sure .gitignore file is located in the root directory of the repository."""
    subprocess.run(f"git status --ignored", shell=True)

def print_folder_structure(folder_path, level=0, num_files_to_print=-1, max_depth=float('inf'), current_depth=0, ignore_dot_folders=True):
    # Default depth: infinite
    if current_depth > max_depth:
        return

    # Get the files and directories in the current directory
    items = os.listdir(folder_path)

    # Loop through the items in the directory
    for i, item in enumerate(sorted(items)):
        if ignore_dot_folders and item.startswith('.'):
            continue
        
        item_path = os.path.join(folder_path, item)

        if os.path.isfile(item_path):
            if num_files_to_print < 0 or i < num_files_to_print:
                print(" " * level * 4 + "- " + item)
            elif i == num_files_to_print:
                print(" " * level * 4 + "- ...")
        else:
            print(" " * level * 4 + "- " + item)

        # Recursively print the contents of subfolders
        if os.path.isdir(item_path):
            print_folder_structure(item_path, level + 1, num_files_to_print, max_depth, current_depth + 1, ignore_dot_folders)


if __name__ == "__main__":
    print_folder_structure(os.getcwd(), max_depth=2,ignore_dot_folders=True)