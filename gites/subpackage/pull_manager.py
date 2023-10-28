import os
import datetime

from gites.subpackage.datastore_json_handler import DatastoreJSONHandler
from gites.subpackage._subprocess_handler import run



# A concise interface function to other module:  
def bulkpush(list_of_repo):
    return GitPullManager.listpull(list_of_repo)

# Complete structure: 
class GitPullManager:
    def __init__(self):
        # granting all informations: 
        self.datastore_json_handler = DatastoreJSONHandler()
        self.root_folder = self.datastore_json_handler.root_dir
        
        all_items = os.listdir(self.root_folder)
        self.repo_list  = [os.path.join(".", item) for item in all_items if os.path.isdir(os.path.join(self.root_folder, item)) and not item.startswith('.')]
        
        # for statistics and summary: 
        self.success_repo = []
        self.failed_repo = []
        self.no_effect_repo = []
        self.repo_that_remote_has_new_update = []
        
        # go to root folder before list pushing. 
        os.chdir(self.root_folder)


    def lpull(self):

        print(f"Totally there are {len(self.repo_list)} repos to work on. They are: {self.repo_list}")
        os.chdir(self.root_folder)

        for repo in self.repo_list:
            """
            chain of commands for each repo 
            (if failed, stop and skip to the next repo):

            git pull
            """
            
            print("+" * 72)
            print(f"Current working directory: {os.getcwd()}")
            print(f"Working on repository: {repo}")
            
            # Git fetch
            return_code, stdout = run(["git", "fetch"], loc = repo)
            if return_code != 0:
                self.no_effect_repo.append(repo)
                self.repo_that_remote_has_new_update.append(repo)
                message = f"""
                This gites lpull command tries to enter each repo within specified root folder, 
                and pull the latest update from the remote server.
                
                By default 'git pull' would not change the local branch if there is
                conflicts between the local and remote branch.
                
                So it is always safe. 
                """
                print(message)
                # Continue: terminate the process for this element, proceed next element in the for-loop
                continue 

            # Git pull
            return_code, stdout = run(["git", "pull"], loc=repo)
            # 3 cases in 'git status': Case 1: there is something new (no need to stop). Case 2 and 3: stop the `listpush` for that repo.
            # Case 3: Other case 
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Git status command failed.")
                continue # type: ignore
            # Case 2: 'Your branch is up to date'
            if "Already up-to-date" in stdout:
                self.no_effect_repo.append(repo)
                print("This repo has no diff detected. Proceed the next repo.")
                continue # type: ignore
            if "Already up-to-date" in stdout:
                self.success_repo.append(repo)
                print("This repo has detected diff and has already pulled. Proceed the next repo.")
                continue # type: ignore
            print("=" * 72)

            
        print("|" * 72)
        print("Add-commit-push completed for all repos in the root folder. Here is the work summary: ")
        print(f"Successful repos (Totally {len(self.success_repo)}): {self.success_repo}")
        print(f"Failed repos (Totally {len(self.failed_repo)}): {self.failed_repo}")
        print(f"No effect repos (Totally {len(self.no_effect_repo)}): {self.no_effect_repo}")
        print(f"Repos that has new updates in the remote server (Totally {len(self.repo_that_remote_has_new_update)}): {self.repo_that_remote_has_new_update}")


# Testing unit: 
if __name__ == "__main__":
    GitPullManager().lpull()

