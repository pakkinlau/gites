import os
import util
from _SubprocessHandler import _SubprocessHandler
from DatastoreJSONHandler import DatastoreJSONHandler

# A concise interface function to other module:  
def initialize_repo(json_name, repo_folder_name, repo_url):
    CreateRepoManager(json_name, repo_folder_name, repo_url).initialize_repo()


# Complete structure: 
class CreateRepoManager:
    def __init__(self, new_created_repo_folder_name, new_created_repo_url):
        self.datastore_json_handler = DatastoreJSONHandler()
        
        # new repo information: 
        self.new_created_repo_folder_name = new_created_repo_folder_name
        self.new_created_repo_url = new_created_repo_url

    def run(self, cmd):
        _SubprocessHandler.run(cmd)

    def check_remote_origin(self, repo_url):
        _, result_stdout = self.run(['git', 'remote', '-v'])
        return repo_url in result_stdout

    def initialize_repo(self):
        
        # Synthesize the path for the newly created repo.
        datastore_json_data = self.datastore_json_handler.data
        root_folder = datastore_json_data["root_directory"]
        full_folder_location = os.path.join(root_folder, self.new_created_repo_folder_name)
        # Future: add the logic that "if the folder is not exist" in `os` module.

        cmd = ['cd', full_folder_location]
        self.run(cmd)
        
        git_folder = os.path.join(full_folder_location, ".git")
        if os.path.exists(git_folder):
            print(f"Deleting existing .git folder at {git_folder}")
            cmd = ['rm', '-rf', git_folder]
            self.run(cmd)

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
            ['git', 'push', '-u', 'origin', 'main'],
        ]

        for cmd in commands_set_1:
            self.run(cmd)

        util.check_and_copy_pre_commit_hook(full_folder_location)

        for cmd in commands_set_2:
            self.run(cmd)

        if self.check_remote_origin(self.repo_url):
            self.run(['git', 'remote', 'set-url', 'origin', self.repo_url])
        else:
            self.run(['git', 'remote', 'add', 'origin', self.repo_url])

        for cmd in commands_set_3:
            self.run(cmd)

if __name__ == "__main__":
    # initialize it: 
    create_repo_manager = CreateRepoManager()
    
    
    datastore_json_name =  create_repo_manager.datastore_json_handler.gites_datastore_json_location
    
    # future development: make it as input() field to let the user just copy things here. 
    repo_folder_name = "Notes field" # Synthesis the full path with the "root_directory" value in the datastore json.
    repo_url = "https://github.com/pakkinlau/BigdataMath.git"

    repo_manager = CreateRepoManager(repo_folder_name, repo_url)
    repo_manager.initialize_repo()