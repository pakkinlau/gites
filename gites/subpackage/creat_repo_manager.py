import os
import util
from ._subprocess_handler import _SubprocessHandler
from .datastore_json_handler import DatastoreJSONHandler


# Complete structure: 
class CreateRepoManager:
    def __init__(self, new_created_repo_folder_name, new_created_repo_url):
        self.datastore_json_handler = DatastoreJSONHandler()
        
        # new repo information: 
        self.new_created_repo_folder_name = new_created_repo_folder_name
        self.new_created_repo_url = new_created_repo_url

    def run(self, cmd):
        _SubprocessHandler().run(cmd)

    def check_remote_origin(self):
        result = self.run(['git', 'remote', '-v'])
        if result is not None:
            _, result_stdout = result
            return repo_url in result_stdout
        return False

    def initialize_repo(self):
        
        # Synthesize the path for the newly created repo.
        datastore_json_data = self.datastore_json_handler.data
        root_folder = datastore_json_data["root_directory"]
        full_folder_location = os.path.join(root_folder, self.new_created_repo_folder_name)

        # Go to that folder. If it is not existed, create it. 
        if not os.path.exists(full_folder_location):
            os.makedirs(full_folder_location)
        os.chdir(full_folder_location)
        
        git_folder = os.path.join(full_folder_location, ".git")
        if os.path.exists(git_folder):
            print(f"Deleting existing .git folder at {git_folder}")
            cmd = ['rm', '-rf', git_folder]
            self.run(cmd)

        commands_set_1 = [
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

        # create readme.md
        file_path = 'readme.md'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('initial document\n')
        else:
            print("File 'readme.md' already exists, skipping creation.")

        for cmd in commands_set_1:
            self.run(cmd)

        util.check_and_copy_pre_commit_hook(full_folder_location)

        for cmd in commands_set_2:
            self.run(cmd)

        list_of_remote_url = self.check_remote_origin()

        if list_of_remote_url:
            self.run(['git', 'remote', 'set-url', 'origin', list_of_remote_url])
        else:
            self.run(['git', 'remote', 'add', 'origin', repo_url])


        for cmd in commands_set_3:
            self.run(cmd)

if __name__ == "__main__":
    # initialize it: 

    # future development: make it as input() field to let the user just copy things here. 
    repo_folder_name = "Factual Value Asset" # Synthesis the full path with the "root_directory" value in the datastore json.
    repo_url = "https://github.com/pakkinlau/Factual-Value-Asset.git"

    create_repo_manager = CreateRepoManager(repo_folder_name, repo_url).initialize_repo()