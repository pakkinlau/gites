# Package: Git-flow-master 

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

To use any of the scripts in this package, simply run them using Python. For example, to check file sizes, run `check_file_size.py`:

```bash
python check_file_size.py
```

Ensure that you have the necessary permissions and dependencies installed to execute the scripts successfully.

## Contributing

Contributions to this repository are highly encouraged! If you have ideas for improvements, additional functionalities, or bug fixes, feel free to open an issue or submit a pull request. Let's collaborate to make Git management even more powerful and user-friendly.

## License

This repository is open-source and available under the [MIT License](LICENSE). You are welcome to use, modify, and distribute the code as per the terms of the license.

Enjoy using the Git-management package! 🚀
