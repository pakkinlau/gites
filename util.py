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
    print("========================================================================")
    print(f"Run: {command}")
    try:
        result = subprocess.run(command, cwd=location, shell=False, text=True, capture_output=True, check=True)
        return_code = result.returncode
        output = result.stdout.strip()
        if return_code == 0:
            print("Command executed successfully!")
        else:
            print(f"This part is not working as expected. Return code: {return_code}.")
            print("Command output:")
            print(output)

        return return_code, output
    except subprocess.CalledProcessError as e:
        print(f"Notice! This command failed. Error: {e}")
        return 1, str(e)

def listpush(list_of_repo: list, tag_message="Automated add-commit-push"):
    success_repo = []
    failed_repo = []

    for repo in list_of_repo:
        # repo expect something like: './Git management'
        print("current location: ")
        print(os.getcwd())
        print(f"+++++++++++++++++++++++++++++++++   Working for the repo:  {repo}   +++++++++++++++++++++++++++++++++")
        try:
            run(["git", "checkout", "main"], location=repo)
            run(["git", "status"], location=repo)
            run(["git", "add", "--all"], location=repo)
            
            # Check and copy pre-commit hook if needed
            check_and_copy_pre_commit_hook(repo)

            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            result, commit_output = run(["git", "commit", "-m", f"{tag_message}. Datetime tag: {current_time}"], location=repo)
            if result != 0:
                print(f"Commit failed. Output:\n{commit_output}")
                failed_repo.append(repo)
        except Exception as e:
            print(f"An error occurred during commit: {e}")
            failed_repo.append(repo)
            continue

        try:
            result, push_output = run(["git", "push", "origin", "main"], location=repo)
            if result == 0:
                success_repo.append(repo)
                print(f"Add-commit-push completed. Tag: {current_time}, {tag_message}")
            else:
                print(f"Push failed. Output:\n{push_output}")
                failed_repo.append(repo)
        except Exception as e:
            print(f"An error occurred during push: {e}")
            failed_repo.append(repo)

        print(f"=====================================================================================")
        print(f"Summary: Successful repos: {success_repo}")
        print(f"Summary: Failed repos: {failed_repo}")
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
