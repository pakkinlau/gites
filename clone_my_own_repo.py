import subprocess
import os
import time 

def clone_repo(remote_url, local_path):
    # status code: 0 = Success, 1 = Fail, 2 = No effect
    try:
        # Check if the repository already exists locally
        if os.path.exists(local_path):
            print(f"Repository '{local_path}' already exists. Skipping cloning.")
            return 2

        # Clone the repository
        subprocess.run(["git", "clone", remote_url, local_path], check=True)
        print(f"Repository '{local_path}' cloned successfully.")

        git_folder_path = os.path.join(local_path, ".git")

        # Check if '.git' folder was cloned successfully
        if not os.path.exists(git_folder_path):
            print(f"Error: '.git' folder was not generated for repository '{local_path}'. Aborting.")
            return 1

        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to clone the repository '{local_path}'.\n{e}")
        return 1
    # The following: try to setup the fresh downloaded repos. 


root_directory = os.path.join(os.path.expanduser("~"), "All_Github_Repos")

list_of_repo = {
    # "Git management": "https://github.com/pakkinlau/your-repo.git", # A repo should not clone itself. 
    "Guides": "https://github.com/pakkinlau/guides.git",
    "Textual notes": "https://github.com/pakkinlau/textual-notes.git",
    "Tutorial template": "https://github.com/pakkinlau/tutorial-template.git",
    "Video materials": "https://github.com/pakkinlau/video-materials.git",
    "JS webpage coding gym": "https://github.com/pakkinlau/js-webpage-coding-gym.git",
    "Python coding gym": "https://github.com/pakkinlau/python-coding-gym.git",
}

if __name__ == "__main__":
    
    start_time = time.time()

    success = []
    failed = []
    no_effect = []
    for repo_name, repo_url in list_of_repo.items():
        local_path = os.path.join(root_directory, repo_name)
        status_message = clone_repo(repo_url, local_path)
        if status_message == 0:
            success.append(repo_name)
        elif status_message == 1:
            failed.append(repo_name)
        elif status_message == 2:  # Changed "else" to "elif"
            no_effect.append(repo_name)
    
    # recording the time spent
    end_time = time.time()
    time_spent = end_time - start_time
    print("Time Spent:", "{:.2f} seconds".format(time_spent))

    # Print the summary
    print("Repositories cloned successfully:", success)
    print("Repositories failed to clone:", failed)
    print("Repositories already existed:", no_effect)
