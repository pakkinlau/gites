# Package: AutoGit

While I am personally use github as a cloud drive to sync and maintain a lot of personal repos. I found the process of typing git command everyday is very repetitive. And such workflow should be streamlined into a single click. 

The goal of this package is to mimic the user experience of using a google drive or one drive. This package tries to memorize your github repo names and their link and record it into a single document, and also the commands are streamlined to be one-clicked. In such way, it save your time on synchronzing the packages when developing your projects. 

## Solutions comparison: 

Compare with `gitpython`:

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

Compare with `vscode source control`:

(We will add real-time update, progress tracking bar to the package in the future)

| Feature             | Your Package         | VS Code Source Control |
|---------------------|----------------------|------------------------|
| JSON Management     | ✔️                    | ❌                      |
| One-Click Sync      | ✔️                    | ✔️                      |
| Git Integration     | ✔️                    | ✔️                      |
| Commit Management   | ✔️                    | ✔️                      |
| Branch Management   | ✔️                    | ✔️                      |
| Diff Viewer         | ✔️                    | ✔️                      |
| History Tracking    | ✔️                    | ✔️                      |
| Conflict Resolution| ✔️                    | ✔️                      |
| User-Friendly UI    | ✔️                    | ✔️                      |
| Customization       | ✔️                    | ✔️                      |
| Remote Repo Support | ✔️                    | ✔️                      |
| Real-time Updates   | ❌                      | ✔️                      |
| Collaboration       | ❌                      | ✔️                      |
| Performance         | Depends on Implem.   | ✔️                      |



## Functionalities of the package: 

- JSON data store: 
    - Memorize what are the repos that you owns and their remote link. You are save it in a particular location and clone all your repos all at once with that JSON as a memory. 
>>
- Autoclone: 
    - Users could clone a list of repos from their json file, which mimic the download actions of using a cloud storage
>>
- Auto-fetch/pull:
    - We will build it later. 
>>
- Auto-large-file-management: 
    - Very often, we might incidently include large size file in our commit, it would stucks the commit-push process. and The package would provide a set of hooks on each of your repos, which provide versatile ability of handling file size error. If there is any large size file detected, that file would be shown in the summary window.
>>
- Auto-large-file-packing-and-push: 
    - If there are large files, our package also included a functionality that providing hooks to all repos. Implementing the pre-commit hook to prevent files larger than 100MB from being committed. This feature ensures that large and unnecessary files do not clutter your repository and slow down your Git workflow.
>>
- Auto-push: 
    - Once you have specified the root folder, that root folder can be considered as your own google drive. You can just sync all the changes with ease, by one click. 
>>


# The journey of auto-packing your repository


Please note that while the table provides a general comparison, it's important to keep in mind that the `gitpython` library is a specialized tool for version control and interacting with Git repositories. It's a mature and widely-used library that's well-suited for managing code repositories. Your custom package seems to be designed for a specific use case involving JSON files and version control, which may not offer the same level of features as a dedicated version control library like `gitpython`. Depending on your project's needs, either option could be appropriate.



## Key Feature

One of the main highlights of this repository is the implementation of a pre-commit hook that prevents files larger than 100MB from being added, committed, and pushed into your Git repositories. This feature is designed to maintain a clean repository history and streamline the "add, commit, push" workflow, ensuring an efficient version control process.


### Usage

- Installation of the package
```bash
pip install autogit
```

- Ensuring your terminal has already logged in your github account:
```bash
abc
```


- Setup the 
```bash
agit init
```

## Future development

1. Consider varying needs from the diversity of potential users. Adding / editing the package to provide more methods.

2. Documentation: Use sphinx and readthedoc to produce an effective documentation to the user. 



## Contributing

Contributions to this repository are highly encouraged! If you have ideas for improvements, additional functionalities, or bug fixes, feel free to open an issue or submit a pull request. Let's collaborate to make Git management even more powerful and user-friendly.

## License

This repository is open-source and available under the [MIT License](LICENSE). You are welcome to use, modify, and distribute the code as per the terms of the license.

Enjoy using the Git-management package! 🚀
