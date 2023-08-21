import subprocess
import os

root_folder = os.path.join(os.path.expanduser("~"), "All_Github_Repos")
os.chdir(root_folder)

location = './Git management'
command = ['git', 'status']
result = subprocess.run(command, cwd=location, shell=True, capture_output=True, text=True)

print(result.returncode)
print(result.stdout)