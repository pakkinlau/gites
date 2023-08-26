import os
import util
from _SubprocessHandler import run
from JSONUpdater import load_data
from _JSONHandler import get_default_userdata_path

# A concise interface function to other module:  
def initialize_repo(json_name, repo_folder_name, repo_url):
    CreateRepoManager(json_name, repo_folder_name, repo_url).initialize_repo()


# Complete structure: 
class CreateRepoManager:
    def __init__(self, json_name, repo_folder_name, repo_url):
        self.json_name = json_name
        self.repo_folder_name = repo_folder_name
        self.repo_url = repo_url

    def run_command(self, cmd):
        run(cmd)

    def check_remote_origin(self, repo_url):
        _, result_stdout = self.run_command(['git', 'remote', '-v'])
        return repo_url in result_stdout

    def initialize_repo(self):
        # Synthesize the path
        json_existing_data = get_default_userdata_path(self.json_name)
        root_folder = json_existing_data["root_directory"]
        full_folder_location = os.path.join(root_folder, self.repo_folder_name)

        cmd = ['cd', full_folder_location]
        self.run_command(cmd)
        
        git_folder = os.path.join(full_folder_location, ".git")
        if os.path.exists(git_folder):
            print(f"Deleting existing .git folder at {git_folder}")
            cmd = ['rm', '-rf', git_folder]
            self.run_command(cmd)

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
            self.run_command(cmd)

        util.check_and_copy_pre_commit_hook(full_folder_location)

        for cmd in commands_set_2:
            self.run_command(cmd)

        if self.check_remote_origin(self.repo_url):
            self.run_command(['git', 'remote', 'set-url', 'origin', self.repo_url])
        else:
            self.run_command(['git', 'remote', 'add', 'origin', self.repo_url])

        for cmd in commands_set_3:
            self.run_command(cmd)

if __name__ == "__main__":
    # Variables that require manual input
    json_name =  # this vakue is provided in another function in Datastore.... class. 
    repo_folder_name = "Notes field" # Synthesis the full path with the "root_directory" value in the datastore json.
    repo_url = "https://github.com/pakkinlau/BigdataMath.git"

    repo_manager = CreateRepoManager(json_name, repo_folder_name, repo_url)
    repo_manager.initialize_repo()