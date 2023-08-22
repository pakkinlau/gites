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
    
    print("=" * 30)
    print(f"Working in the {os.path.abspath(location)} folder...")
    print(f"Run: {command}")
    
    # there are 3 possible cases: Successful-non-zero, successful-zero, Failed-subprocess. 
    try:
        result = subprocess.Popen(
            command,
            cwd=location,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Capture the standard output and standard error

        # these are byte output
        stdout, stderr = result.communicate()
        # these are string output
        string_stdout = stdout.decode('utf-8')
        string_stderr = stderr.decode('utf-8')
        # this is integer
        return_code = result.returncode

        # Consider only shows the terminal communications if some special cases happens. 
        # But hold always-printing for development purpsoe 
        print("Returned exit code:", return_code)
        print("Standard Output:", string_stdout)
        print("Standard Error:", string_stderr)

        # Case 2: Successful-zero
        if return_code == 0:
            # Only print success if `0` code is received. 
            print("Command executed successfully!")
        # Case 1: Successful-non-zero
        else:
            print("Command failed. Please check the above messages")
        return return_code, string_stdout
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
    no_effect_repo = []

    for repo in list_of_repo:
        print("+" * 72)
        print(f"Current working directory: {os.getcwd()}")
        print(f"Working on repository: {repo}")
        
        return_code, _ = run(["git", "checkout", "main"], location=repo)
        # this if-block terminate the `listpush` if there is any non-zero exit code. 
        # Case 1: It is already in 'main', then return code is 0. 
        # Case 2: Other cases. 
        if return_code != 0:
            # Continue: terminate the process for this element, proceed next element in the for-loop
            failed_repo.append(repo)
            continue
        
        return_code, stdout = run(["git", "status"], location=repo)
        # 3 cases in 'git status': Case 1: there is something new (no need to stop). Case 2 and 3: stop the `listpush` for that repo.
        # Case 3: Other case 
        if return_code != 0:
            failed_repo.append(repo)
            continue
        # Case 2: 'Your branch is up to date'
        if "our branch is up to date" in stdout:
            no_effect_repo.append(repo)
            continue
        
        return_code, _ = run(["git", "add", "--all"], location=repo)
        # `git add` won't tell much from the output.
        if return_code != 0:
            failed_repo.append(repo)
            continue
        
        # Commit: 
        timetag_for_commit = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        commit_command = ["git", "commit", "-m", f"{tag_message}. Datetime tag: {timetag_for_commit}"]
        
        return_code, stdout = run(commit_command, location=repo)
        # Case 2: Any other case
        if return_code != 0:
            failed_repo.append(repo)
            continue
        # Case 3 (Trivial): The staging area is empty (But it is most probably blocked due to the previous `git add` control flow)
        if "nothing to commit" in stdout:
            print("No changes to commit.")
            no_effect_repo.append(repo)
            continue
        print(f"Commit successful. Output:\n{stdout}")
        
        # Push: 
        push_command = ["git", "push", "origin", "main"]
        _, push_output = run(push_command, location=repo)
        
        if "Total" in push_output:
            success_repo.append(repo)
            print(f"Add-commit-push completed. Tag: {timetag_for_commit}, {tag_message}")
        else:
            print(f"Push failed. Output:\n{push_output}")
            failed_repo.append(repo)

        print("=" * 72)
        
    print("Summary:")
    print(f"Successful repos: {success_repo}")
    print(f"Failed repos: {failed_repo}")
    print(f"No effect repos: {no_effect_repo}")



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
