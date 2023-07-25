import subprocess
import os
import util

#####################
# Update information here: 


full_folder_location = r"D:\All_programming_projects\Video materials"
repo_url = "https://github.com/pakkinlau/Video-material.git" 


#####################
# The script is in the following:

def run(command, location=os.getcwd()):
    try:
        print(f"Run: {command}")
        subprocess.run(f"{command}", shell=True, cwd=location, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{command} failed.")
        return


command1 = f"git init"
command2 = f"git add ."
command3 = f'git commit -m "first commit"'
command4 = f"git checkout -b main" # checkout switch between branch. -b create a new branch and switch to it. 
command5 = f"git remote add origin {repo_url}" 
command6 = f"git push -u origin main"

run(command1)
util.check_and_copy_pre_commit_hook(full_folder_location)
run(command2)
run(command3)
run(command4)
run(command5)
run(command6)
