import subprocess
import os

def clone_repo(remote_url, local_path):
    try:
        if not os.path.exists(local_path):
            subprocess.run(["git", "clone", remote_url, local_path], check=True)
            print(f"Repository '{local_path}' cloned successfully.")
        else:
            print(f"Local repository '{local_path}' already exists. Skipping clone.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to clone the repository '{local_path}'.\n{e}")

root_directory = r"...."

list_of_repo = {
    "Git management": "https://github.com/pakkinlau/your-repo.git",
    "Guides": "https://github.com/pakkinlau/guides.git",
    "Python coding gym": "https://github.com/pakkinlau/python-coding-gym.git",
    "Textual notes": "https://github.com/pakkinlau/textual-notes.git",
    "Tutorial template": "https://github.com/pakkinlau/tutorial-template.git",
    "Video materials": "https://github.com/pakkinlau/video-materials.git",
    "JS webpage coding gym": "https://github.com/pakkinlau/js-webpage-coding-gym.git"
}

if __name__ == "__main__":
    for repo_name, repo_url in list_of_repo.items():
        local_path = os.path.join(root_directory, repo_name)
        clone_repo(repo_url, local_path)
