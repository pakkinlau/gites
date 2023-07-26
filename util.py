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

def run(command, location="must specify location"):
    print("========================================================================")
    result = None  # Initialize result with None
    try:
        print(f"Run: {command}")
        result = subprocess.run(command, cwd=location) #, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True, shell=True)
        return_code = result.returncode
        if return_code == 0:
            print("Command executed successfully!")
        else:
            print(f"This part is not working as expected. Return code: {return_code}. Read the git message for information")

        return return_code
    except Exception as e:
        print(f"Notice! This command failed. Error: {e}")
        return result  # Return the initial value of result in case of an exception


def listpush(list_of_repo: list, tag_message="Automated add-commit-push"):
    
    success_repo = []
    failed_repo = []
    # print the header for separating the message for each repo
    
    for repo in list_of_repo:
        os.system(f"cd {repo}")
        print(f"+++++++++++++++++++++++++++++++++   Working for the repo:  {repo}   +++++++++++++++++++++++++++++++++")
        try:
            run("git checkout main",location=repo)
            run("git status",location=repo)
            run("git add --all",location=repo)
            # subprocess.run("git checkout main", shell=True, cwd=repo)
            # subprocess.run("git status", shell=True, cwd=repo)
            # subprocess.run("git add --all", shell=True, cwd=repo)
            
            # Check and copy pre-commit hook if needed
            check_and_copy_pre_commit_hook(repo)

            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            result = run(f'git commit -m"{tag_message}. Datetime tag: {current_time}"',location=repo)
            # result = subprocess.run(f'git commit -m"{tag_message}. Datetime tag: {current_time}"', shell=True, cwd=repo, stderr=subprocess.PIPE)    # stdout=subprocess.PIPE
            if result != 0:
                print(result)  # Check if the git commit command returned non-zero exit code
        except subprocess.CalledProcessError as e:
            print(f"Commit failed with error message: {e.stderr.decode().strip()}")
            failed_repo.append(repo)
            return
        # If commit is successful, continue with the git push command
        try:
            run("git push origin main",location=repo)
            # subprocess.run(f"git push origin main", shell=True, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            success_repo.append(repo)
            print(f"Add-commit-push completed. Tag: {current_time}, {tag_message}")
        except subprocess.CalledProcessError as e:
            print(f"Push failed with error message: {e.stderr.decode().strip()}")
            failed_repo.append(repo)
    print(f"=====================================================================================")
    print(f"summary: successed repo: {success_repo}")
    print(f"summary: failed repo: {failed_repo}")
    print(f"=====================================================================================")

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
