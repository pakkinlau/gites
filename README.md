# Package: AutoGit

While I am personally use github as a cloud drive to sync and maintain a lot of personal repos. I found the process of typing git command everyday is very repetitive. And such workflow should be streamlined into a single click. 

This package tries to save your time on synchronzing the packages that you own. The goal of this package is to mimic the user experience of using a google drive or one drive. 

## Solution comparison: 

A comparison of the functionality between two packages:

| Feature / Capability            | Your Custom Package       | gitpython Library         |
|---------------------------------|---------------------------|---------------------------|
| Manage JSON file                | ✔️ Custom JSON handling   | ❌ JSON handling only     |
| Create Git repositories         | ✔️                        | ✔️                        |
| Commit changes                  | ✔️                        | ✔️                        |
| Push changes to remote          | ✔️                        | ✔️                        |
| Pull changes from remote        | ❌ (Not mentioned)        | ✔️                        |
| Sync with one click             | ✔️ Custom implementation  | ❌ (Not mentioned)        |
| Subprocess management           | ✔️                        | ❌                        |
| Pre-commit hooks                | ✔️ Custom implementation  | ❌                        |
| Custom timing functionality     | ✔️                        | ❌                        |
| Comprehensive error handling    | ✔️                        | ✔️                        |
| JSON configuration options      | ✔️ Custom implementation  | ❌                        |
| Flexibility for expansion       | ✔️                        | ✔️                        |
| Popularity and community support| ❌ (Not mentioned)        | ✔️ Well-established       |
|                                 |


## Functionalities: 

- JSON data store: 
    - Memorize what are the repos that you owns and their remote link. You are save it in a particular location and clone all your repos all at once with that JSON as a memory. 

- Autoclone: 
    - Users could clone a list of repos from their json file, which mimic the download actions of using a cloud storage

- Auto-pull:

- Auto-large-file-management: 
    - Very often, we might incidently include large size file in our commit, it would stucks the commit-push process. and The package would provide a set of hooks on each of your repos, which provide versatile ability of handling file size error. If there is any large size file detected, that file would be shown in the summary window.

- Auto-large-file-packing-and-push: 
    - If there are large files, our package also included a functionality that could streamline the process of "compressing large file and then pack it up into N pieces smaller than 100MB. Which mimics the git-hub large file system.

- Auto-push: 
    - Once you have specified the root folder, that root folder can be considered as your own google drive. You can just sync all the changes with ease, by one click. 



# The journey of auto-packing your repository

While 

Please note that while the table provides a general comparison, it's important to keep in mind that the `gitpython` library is a specialized tool for version control and interacting with Git repositories. It's a mature and widely-used library that's well-suited for managing code repositories. Your custom package seems to be designed for a specific use case involving JSON files and version control, which may not offer the same level of features as a dedicated version control library like `gitpython`. Depending on your project's needs, either option could be appropriate.


Welcome to the **Git flow master** repository! This repository is a versatile package containing multiple useful functions and tools designed to enhance your Git workflow and repository management. It provides a collection of Python scripts with various functionalities to make version control easier and more efficient.

## Key Feature

One of the main highlights of this repository is the implementation of a pre-commit hook that prevents files larger than 100MB from being added, committed, and pushed into your Git repositories. This feature is designed to maintain a clean repository history and streamline the "add, commit, push" workflow, ensuring an efficient version control process.

## Pre-commit Hook Script

As mentioned earlier, the `push_repos.py` file in this package implements the pre-commit hook to prevent files larger than 100MB from being committed. This feature ensures that large and unnecessary files do not clutter your repository and slow down your Git workflow.

## Other package Contents

This repository contains the following Python scripts, each serving a specific purpose:

1. `check_file_size.py`: A script that allows you to check the size of files in your repository and identify any files exceeding a specified limit, such as 100MB.

2. `clone_my_own_repo.py`: A script that simplifies the process of cloning your own repositories hosted on Git platforms like GitHub or GitLab.

3. `create_repo.py`: A script that streamlines the creation of new Git repositories, making it easy to initiate version control for your projects.

4. `print_folder_file_tree.py`: A script that generates a tree-like representation of the files and folders in your repository, helping you visualize the structure of your project.

5. `util.py`: A utility script containing helper functions used by other scripts within the package.

### Usage

- Installation of the package
```bash
pip install autogit
```



- Setup the 
```bash
agit init
```



Ensure that you have the necessary permissions and dependencies installed to execute the scripts successfully.

## Contributing

Contributions to this repository are highly encouraged! If you have ideas for improvements, additional functionalities, or bug fixes, feel free to open an issue or submit a pull request. Let's collaborate to make Git management even more powerful and user-friendly.

## License

This repository is open-source and available under the [MIT License](LICENSE). You are welcome to use, modify, and distribute the code as per the terms of the license.

Enjoy using the Git-management package! 🚀
