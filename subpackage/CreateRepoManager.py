import os
import util
from _SubprocessHandler import run
from JSONUpdater import load_data

# A concise interface function to other module:  
def initialize_repo(repo_url, full_folder_location):
    CreateRepoManager(repo_url, full_folder_location).initialize_repo()


# Complete structure: 
class CreateRepoManager:
    def __init__(self, repo_url, full_folder_location):
        self.repo_url = repo_url
        self.full_folder_location = full_folder_location

    def run_command(self, cmd):
        run(cmd)

    def check_remote_origin(self, repo_url):
        _, result_stdout = self.run_command(['git', 'remote', '-v'])
        return repo_url in result_stdout

    def initialize_repo(self):
        cmd = ['cd', self.full_folder_location]
        self.run_command(cmd)
        
        git_folder = os.path.join(self.full_folder_location, ".git")
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

        util.check_and_copy_pre_commit_hook(self.full_folder_location)

        for cmd in commands_set_2:
            self.run_command(cmd)

        if self.check_remote_origin(self.repo_url):
            self.run_command(['git', 'remote', 'set-url', 'origin', self.repo_url])
        else:
            self.run_command(['git', 'remote', 'add', 'origin', self.repo_url])

        for cmd in commands_set_3:
            self.run_command(cmd)

if __name__ == "__main__":
    # A variable that requires manual input
    repo_url = "https://github.com/pakkinlau/BigdataMath.git"
    
    root_folder = 1 # I need to resolve "how the script recognize the default json path"
    repo_folder_name = 2
    
    full_folder_location = "root folder" + "repo folder name"

    repo_manager = CreateRepoManager(repo_url, full_folder_location)
    repo_manager.initialize_repo()