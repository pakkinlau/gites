import os
import subprocess
import shutil
import datetime

def check_and_copy_pre_commit_hook(repo_location):
    hooks_dir = os.path.join(repo_location, ".git", "hooks")
    pre_commit_hook_path = os.path.join(hooks_dir, "pre-commit")
    pre_made_hook_path = os.path.join(os.path.dirname(__file__), "My hooks", "pre-commit")  # Replace this with the actual path of your pre-made hook.

    if not os.path.exists(hooks_dir):
        os.makedirs(hooks_dir)

    if not os.path.exists(pre_commit_hook_path):
        print("Copying pre-commit hook...")
        shutil.copy(pre_made_hook_path, pre_commit_hook_path)
        os.chmod(pre_commit_hook_path, 0o755)
        print("Pre-commit hook copied.")
    else:
        print("Pre-commit hook already exists.")

def run(command, location):
    """Run a command and capture its output and return code."""
    
    # Logging
    print("=" * 72)
    print(f"Run: {command}")
    print(f"Working in the {os.path.abspath(location)} folder...")
    
    # there are 3 possible cases: Successful-non-zero, successful-zero, Failed-subprocess. 
    try:
        result = subprocess.Popen(
            command,
            cwd=location,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Capture the standard output and standard error
        stdout, stderr = result.communicate()
        return_code = result.returncode
        output = stdout.strip()
        error_output = stderr.strip()

        print("Returned exit code:", return_code)
        print("Standard Output:", stdout.decode('utf-8'))
        print("Standard Error:", stderr.decode('utf-8'))
        print(f"Output: {output}")
        print(f"Error output: {error_output}")
        # output = result.stdout.strip()
        # error_output = result.stderr.strip()
        
        # Case 2: Successful-zero
        if return_code == 0:
            print("Command executed successfully!")
        # Case 1: Successful-non-zero
        else:
            print("Command failed. Please check the above messages")
        return return_code
    # Case 3: Failed-subprocess
    # Case 3a: If there is any non-zero return code
    except subprocess.CalledProcessError as e:
        print("Subprocess failed with exit code:", e.returncode)
        print("Error output:", e.stderr)
    # Case 3b: Generic catch-all for any other exceptions. 
    except Exception as e:
        print("An error occurred:", e)
        

def listpush(list_of_repo: list, tag_message="Automated add-commit-push"):
    """Automate adding, committing, and pushing in multiple repositories."""
    success_repo = []
    failed_repo = []

    for repo in list_of_repo:
        print("+" * 72)
        print(f"Current working directory: {os.getcwd()}")
        print(f"Working on repository: {repo}")
        
        return_code = run(["git", "checkout", "main"], location=repo)
        if return_code != 0:
            return
        
        return_code = run(["git", "status"], location=repo)
        if return_code != 0:
            return
        
        return_code = run(["git", "add", "--all"], location=repo)
        if return_code != 0:
            return
        
        try:
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            commit_command = ["git", "commit", "-m", f"{tag_message}. Datetime tag: {current_time}"]
            _, commit_output = run(commit_command, location=repo)
            
            if "nothing to commit" in commit_output:
                print("No changes to commit.")
            else:
                print(f"Commit successful. Output:\n{commit_output}")
                
                push_command = ["git", "push", "origin", "main"]
                _, push_output = run(push_command, location=repo)
                
                if "Total" in push_output:
                    success_repo.append(repo)
                    print(f"Add-commit-push completed. Tag: {current_time}, {tag_message}")
                else:
                    print(f"Push failed. Output:\n{push_output}")
                    failed_repo.append(repo)
        except Exception as e:
            print(f"An error occurred: {e}")
            failed_repo.append(repo)

        print("=" * 72)
        
    print("Summary:")
    print(f"Successful repos: {success_repo}")
    print(f"Failed repos: {failed_repo}")



def get_files_bigger_than_100mb(folder_path):
    file_list = []

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to megabytes

            if file_size_mb > 100:
                file_list.append(os.path.relpath(file_path, start=folder_path))

    return file_list

def clean_undone_commit():
    """When crashes (eg: some large files included in the commit), clean undone commit by this."""
    subprocess.run(f"git reset --soft HEAD~", shell=True)


def check_ignored_path():
    """Before this, make sure .gitignore file is located in the root directory of the repository."""
    subprocess.run(f"git status --ignored", shell=True)
