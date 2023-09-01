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
            print("Failed. Code: s5ws2w")
            continue
        
        return_code, stdout = run(["git", "status"], location=repo)
        # 3 cases in 'git status': Case 1: there is something new (no need to stop). Case 2 and 3: stop the `listpush` for that repo.
        # Case 3: Other case 
        if return_code != 0:
            failed_repo.append(repo)
            print("Failed. Code: 1sd2a")
            continue
        # Case 2: 'Your branch is up to date'
        if "nothing to commit, working tree clean" in stdout:
            no_effect_repo.append(repo)
            print("No effect to the repo. Code: 2sd32")
            continue
        
        return_code, _ = run(["git", "add", "--all"], location=repo)
        # `git add` won't tell much from the output.
        if return_code != 0:
            failed_repo.append(repo)
            print("Failed. Code: a1sd32")
            continue
        
        # Commit: 
        timetag_for_commit = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        commit_command = ["git", "commit", "-m", f"{tag_message}. Datetime tag: {timetag_for_commit}"]
        
        return_code, stdout = run(commit_command, location=repo)
        # Case 2: Any other case
        if return_code != 0:
            failed_repo.append(repo)
            print("Failed. Code: 1zsxer2")
            continue
        # Case 3 (Trivial): The staging area is empty (But it is most probably blocked due to the previous `git add` control flow)
        if "nothing to commit" in stdout:
            print("No changes to commit.")
            no_effect_repo.append(repo)
            print("No effect to the repo. Code: t5gs2")
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