import os

from ._subprocess_handler import run
from ._timing import timing
from gites.subpackage.datastore_json_handler import DatastoreJSONHandler



# Complete structure: 
class RepoCloner:
    def __init__(self):
        self.datastore_json_handler = DatastoreJSONHandler()
        self.root_folder = self.datastore_json_handler.root_dir
        self.list_of_repo_details = self.datastore_json_handler.list_of_repo_details

        """
        # old settings
        self.config_file_path = config_file_path
        self.root_directory = ""
        self.repositories = []
        """

        self.success = []
        self.failed = []
        self.no_effect = []

    @timing
    def lclone(self):
        # self.load_config()
        self.clone_repositories()
        self.print_summary()

    """
    def load_config(self):
        with open(self.config_file_path, "r") as config_file:
            config = json.load(config_file)
        self.root_directory = config["root_directory"]
        self.repositories = config["repositories"]
    """

    def clone_repo(self, remote_url, local_path):
        
        # check whether that folder already exists AND it is not empty.
        # It won't bother any existing folder. 
        if os.path.exists(local_path) and any(os.listdir(local_path)):
            print(f"Repository '{local_path}' already exists. Skipping cloning.")
            return 2
        # Don't need to create folder, because git clone would take care of it.
        
        # execute git command
        # go to the root folder
        os.chdir(self.root_folder)
        command = ["git", "clone", remote_url]
        return_code, _ = run(command, loc = self.root_folder)
        
        # to verify the clone, by checking whether the `.git` exist.
        git_folder_path = os.path.join(local_path, ".git")
        if not os.path.exists(git_folder_path):
            print(f"Error: '.git' folder was not generated for repository '{local_path}'. Aborting.")
            # could put a strong SystemExit here
        
        # return status code 
        return return_code

    def clone_repositories(self):
        
        # go to the root folder
        os.chdir(self.root_folder)
        
        for repo_info in self.list_of_repo_details:
            repo_name = repo_info["name"]
            repo_url = repo_info["remote_url"]
            local_path = os.path.join(self.root_folder, repo_name)
            status_message = self.clone_repo(repo_url, local_path)
            if status_message == 2:
                self.no_effect.append(repo_name)
                continue
            elif status_message !=0:
                self.failed.append(repo_name)
                continue
            elif status_message == 0:
                self.success.append(repo_name)
                print(f"Repository '{repo_name}' cloned successfully.")

    def print_summary(self):
        print("Repositories cloned successfully:", self.success)
        print("Repositories failed to clone:", self.failed)
        print("Repositories already existed:", self.no_effect)

if __name__ == "__main__":
    cloner = RepoCloner()
    cloner.lclone()