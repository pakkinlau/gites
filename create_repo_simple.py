import subprocess
import os
import util

#####################
# Update information here: 

full_folder_location = r"D:\All_programming_projects\Video materials"
repo_url = "https://github.com/pakkinlau/Video-material.git" 

#####################
# The script is in the following:

def run(command):
    subprocess.run(command)
    print("========================")

def check_remote_origin():
    result = subprocess.run("git remote -v", capture_output=True, text=True, shell=True)
    existing_remotes = result.stdout
    return repo_url in existing_remotes

def update_remote_origin():
    subprocess.run(f"git remote set-url origin {repo_url}", shell=True)

command1 = f"git init"
command2 = f"git add ."
command3 = f'git commit -m "first commit"'
command4 = f"git branch -M main"
command5 = f"git remote -v"
command6 = f"git push -u origin main"

run(command1)
util.check_and_copy_pre_commit_hook(full_folder_location)
run(command2)
run(command3)
run(command4)

if check_remote_origin():
    update_remote_origin()
else:
    run(f"git remote add origin {repo_url}")

run(command6)


