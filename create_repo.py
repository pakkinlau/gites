import subprocess
import os
import util
from SubprocessHandler import run



def check_remote_origin(repo_url):
    # This git command return info about the remote repo associated with your Git repo. 
    cmd = ['git','remote','-v']
    loc = os.getcwd()
    result = run(cmd, loc)
    result = subprocess.run("git remote -v", capture_output=True, text=True, shell=True)
    existing_remotes = result.stdout
    return repo_url in existing_remotes

def update_remote_origin(repo_url):
    subprocess.run(f"git remote set-url origin {repo_url}", shell=True)

def delete_git_folder(location):
    git_folder = os.path.join(location, ".git")
    if os.path.exists(git_folder):
        print(f"Deleting existing .git folder at {git_folder}")
        run(f"rm -rf {git_folder}")

def main():
    full_folder_location = r"D:\All_programming_projects\Textual notes"
    repo_url = "https://github.com/pakkinlau/Textual-notes.git" 

    run(f"cd {full_folder_location}")
    # Delete the .git folder if it exists
    delete_git_folder(full_folder_location)

    commands_set_1 = [
        ['echo', 'initial document', '>>', 'firstfile.txt'],
        ['git', 'init'],
]
    commands_set_2 = [
        ['git', 'add', '.'],
        ['git', 'commit', '-m', 'first commit'],
        ['git', 'checkout', '-b', 'main'],
]
    commands_set_3 = [
        ['git', 'remote', '-v'],
        ['git', 'push', '-u', 'origin', 'main']
]
    for cmd in commands_set_1:
        run(cmd)

    util.check_and_copy_pre_commit_hook(full_folder_location)
    
    for cmd in commands_set_2:
        run(cmd)

    # config the origin url for this repo
    if check_remote_origin(repo_url):
        update_remote_origin(repo_url)
    else:
        run(f"git remote add origin {repo_url}")

    for cmd in commands_set_3:
        run(cmd)

# Testing unit: 
if __name__ == "__main__":
    main()
