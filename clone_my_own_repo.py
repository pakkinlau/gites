import os
import time 
import json

from SubprocessHandler import run


class Timer:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()
        self.time_spent = self.end_time - self.start_time

class RepoCloner:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.root_directory = ""
        self.repositories = []
        self.success = []
        self.failed = []
        self.no_effect = []

    def clone(self):
        self.load_config()
        self.clone_repositories()
        self.print_summary()

    def load_config(self):
        with open(self.config_file_path, "r") as config_file:
            config = json.load(config_file)
        self.root_directory = config["root_directory"]
        self.repositories = config["repositories"]

    def clone_repo(self, remote_url, local_path):
        if os.path.exists(local_path) and any(os.listdir(local_path)):
            print(f"Repository '{local_path}' already exists. Skipping cloning.")
            return 2
        command = ["git", "clone", remote_url, local_path]
        run(command, check=True)
        print(f"Repository '{local_path}' cloned successfully.")
        
        git_folder_path = os.path.join(local_path, ".git")
        if not os.path.exists(git_folder_path):
            print(f"Error: '.git' folder was not generated for repository '{local_path}'. Aborting.")
            return 1
        return 0

    def clone_repositories(self):
        for repo_info in self.repositories:
            repo_name = repo_info["name"]
            repo_url = repo_info["remote_url"]
            local_path = os.path.join(self.root_directory, repo_name)
            status_message = self.clone_repo(repo_url, local_path)
            if status_message == 0:
                self.success.append(repo_name)
            elif status_message == 1:
                self.failed.append(repo_name)
            elif status_message == 2:
                self.no_effect.append(repo_name)

    def print_summary(self):
        print("Repositories cloned successfully:", self.success)
        print("Repositories failed to clone:", self.failed)
        print("Repositories already existed:", self.no_effect)

if __name__ == "__main__":
    with Timer() as timer:
        cloner = RepoCloner("gpf-config.json")
        cloner.clone()
    print("Time Spent:", "{:.2f} seconds".format(timer.time_spent))