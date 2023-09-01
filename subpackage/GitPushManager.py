import os
from _SubprocessHandler import run
import datetime
from DatastoreJSONHandler import DatastoreJSONHandler

# A concise interface function to other module:  
def bulkpush(list_of_repo):
    return GitPushManager.listpush(list_of_repo)

# Complete structure: 
class GitPushManager:
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
        
        # go to root folder before list pushing. 
        os.chdir(self.root_folder)


    def lpush(self):

        print(f"Totally there are {len(self.repo_list)} repos to work on. They are: {self.repo_list}")
        os.chdir(self.root_folder)

        for repo in self.repo_list:
            print("+" * 72)
            print(f"Current working directory: {os.getcwd()}")
            print(f"Working on repository: {repo}")
            
            # Git checkout
            return_code, _ = run(["git", "checkout", "main"], loc = repo)
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Gheckout failed")
                # Continue: terminate the process for this element, proceed next element in the for-loop
                continue 

            # Git status
            return_code, stdout = run(["git", "status"], loc=repo)
            # 3 cases in 'git status': Case 1: there is something new (no need to stop). Case 2 and 3: stop the `listpush` for that repo.
            # Case 3: Other case 
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Git status command failed.")
                continue # type: ignore
            # Case 2: 'Your branch is up to date'
            if "nothing to commit, working tree clean" in stdout:
                self.no_effect_repo.append(repo)
                print("This repo is new. Proceed the next repo.")
                continue # type: ignore

            # Git add all
            return_code, _ = run(["git", "add", "--all"], loc=repo)
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Failed. Code: a1sd32")
                continue # type: ignore

            # Git commit
            tag_message="Automated add-commit-push"
            timetag_for_commit = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            commit_command = ["git", "commit", "-m", f"{tag_message}. Datetime tag: {timetag_for_commit}"]
            return_code, stdout = run(commit_command, loc=repo)
            # Case 2: Any other case
            if return_code != 0:
                self.failed_repo.append(repo)
                print("Failed. Code: 1zsxer2")
                continue # type: ignore
            # Case 3 (Trivial): The staging area is empty (But it is most probably blocked due to the previous `git add` control flow)
            if "nothing to commit" in stdout:
                print("No changes to commit.")
                self.no_effect_repo.append(repo)
                print("No effect to the repo. Code: t5gs2")
                continue # type: ignore
            print(f"Commit successful. Output:\n{stdout}")

            # Git push origin main
            push_command = ["git", "push", "origin", "main"]
            _, push_output = run(push_command, loc=repo)
            if "Total" in push_output or not push_output:
                self.success_repo.append(repo)
                # Future development: Scrape the terminal output and collect those data to summary variable.
                print("Push completed")
            else:
                print(f"Push failed. Output:\n{push_output}")
                self.failed_repo.append(repo)
            print("=" * 72)

            
        print("|" * 72)
        print("Add-commit-push completed for all repos in the root folder. Here is the work summary: ")
        print(f"Successful repos (Totally {len(self.success_repo)}): {self.success_repo}")
        print(f"Failed repos (Totally {len(self.failed_repo)}): {self.failed_repo}")
        print(f"No effect repos (Totally {len(self.no_effect_repo)}): {self.no_effect_repo}")

# Testing unit: 
if __name__ == "__main__":
    GitPushManager().lpush()

