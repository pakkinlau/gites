import subprocess
import os 

from datetime import datetime
now = datetime.now()

def push():
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") # 16/09/2022 22:29:34

    """ Change your file location here """
    os.chdir(r"C:\Users\kinla\All_programming_projects") 
    subprocess.run('git status',shell=True)
    subprocess.run('git add --all',shell=True)

    """ Change your upload tag here"""
    subprocess.run(f'git commit -m"{dt_string}"',shell=True)
    subprocess.run(f'git push origin main',shell=True)

    print(f"Completed. Tag: {dt_string}")

def clean_undone_commit():
    """When crashes (eg: some large files included in the commit), clean undone commit by this."""
    subprocess.run(f'git reset --soft HEAD~',shell=True)

def check_ignored_path():
    """Before this, make sure .gitignore file is located in the root directory of the repository."""
    subprocess.run(f'git status --ignored',shell=True)