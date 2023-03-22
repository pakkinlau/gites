import subprocess

# 1. change the following information before creating a new repo.
# 2. Remember to create repos in the website first.
# 3. Make sure the repo is empty and clean initial state.
# 4. Make sure git LFS is installed on the computer. Download link: https://git-lfs.com/

full_folder_location = r"C:\Users\kinla\All_programming_projects\JS webpage coding gym"
repo_url = "https://github.com/pakkinlau/JS-webpage-coding-gym.git" # 

command1 = f"git init"
command2 = f"git checkout -b main"
command3 = f"git remote add origin {repo_url}"
command4 = f"git config --global core.autocrlf false"
command5 = f"git config --global http.postBuffer 2147483648"

command6 = f"git lfs install"
command7 = f"git lfs track '*.zip' '*.tar.gz' '*.tar' '*.mp4' '*.pdf'"

commit = "first commit"
command8 = "git add .gitattributes"

# Add large files to Git LFS before adding and committing them
command9 = "git lfs track '*.zip' '*.tar.gz' '*.tar' '*.mp4' '*.pdf'"
command10 = "git add ."
command11 = f'git commit -m "{commit}"'

command12 = f"git push -u origin main"

def run(command):
    print(f"Run: {command}")
    subprocess.run(command, shell=True, cwd=full_folder_location)

run(command1)
run(command2)
run(command3)
run(command4)
run(command5)
run(command6)
run(command7)
run(command8)
run(command9)
run(command10)
run(command11)
run(command12)