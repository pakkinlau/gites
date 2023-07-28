# Git-management Repository

Welcome to the **Git-management** repository! This repository is designed to enhance your Git workflow by providing a useful pre-commit hook that prevents files larger than 100MB from being added, committed, and pushed into your Git repositories. This can significantly improve the overall performance and maintain a clean and efficient repository history.

## Selling Point

The primary selling point of this repository is the implementation of a pre-commit hook that enforces a file size limit of 100MB. When using this pre-commit hook, it becomes impossible to add, commit, and push files exceeding this limit, which ensures that large and unnecessary files do not clutter your repository and slow down the "add commit push" workflow.

## Pre-commit Hook Script

The pre-commit hook is implemented in the `push_repos.py` file. This Python script utilizes the Git hooks mechanism to automatically check the size of files being committed. If it detects any files larger than 100MB, it will prevent the commit from proceeding, allowing you to rectify the situation and optimize your repository's file structure.

### Usage

To utilize the pre-commit hook in your Git repositories, follow these steps:

1. Copy the `push_repos.pyy` script into the `.git/hooks/` directory of your repository.

2. Ensure the script has executable permissions. If not, use the following command to grant the required permission:
   ```bash
   chmod +x .git/hooks/push_repos.py
   ```

3. From now on, whenever you attempt to make a commit, the pre-commit hook will automatically check for files larger than 100MB. If such files are found, the commit will be halted, providing you with the list of offending files to address the issue.

**Note:** The script assumes that your root folder is specified in the `root_folder` variable within the script. Make sure to modify this variable to match the path of your repository.

## Repository Structure

This repository contains the following files:

- `push_repos.py`: The Python script that implements the pre-commit hook preventing files larger than 100MB.

## Contributing

Contributions to this repository are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request. Let's work together to make Git management more effective and streamlined.

## License

This repository is open-source and available under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.

## About the Author

This repository is maintained by [Your Name], a passionate developer interested in optimizing Git workflows and making version control easier for everyone.

Happy coding! 🚀
