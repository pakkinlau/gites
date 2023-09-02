# Package: gites

![Alt text](images/gites.png)
Image: The photos of "gites".

While I am personally use github as a cloud drive to sync and maintain a lot of personal repos. I found the process of typing git command everyday is very repetitive. And such workflow should be streamlined into a single click. 

The goal of this package is to mimic the user experience of using a google drive or one drive. This package tries to memorize your github repo names and their link and record it into a single document, and also the commands are streamlined to be one-clicked. In such way, it save your time on synchronzing the packages when developing your projects. 

## Solutions comparison: 

Compare with `gitpython`:

| Feature / Capability            | This Package              | gitpython Library         |
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


| Feature             | This Package         | VS Code Source Control |
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

(Note: We will add real-time update, progress tracking bar to the package in the future to make the package to be more competitive)

---

## Functionalities of the package: 

- JSON data store: 
    - Memorize what are the repos that you owns and their remote link. You are save it in a particular location and clone all your repos all at once with that JSON as a memory.
>>
- Auto-large-file-management: 
    - Very often, we might incidently include large size file in our commit, it would stucks the commit-push process. and The package would provide a set of hooks on each of your repos, which provide versatile ability of handling file size error. If there is any large size file detected, that file would be shown in the summary window.
>>
- `gites lpush`:
    - Bulk pushing your repos from a local folder of your computer. Once you have specified the root folder, that root folder can be considered as your own google drive. You can just sync all the changes with ease, by one click. 
![Alt text](images/push demo.png)


- `gites lclone`: 
    - Bulk cloning your repos from the datastore json. It is still in testing.
>>
- `gites lfetch`:
    - Bulk fetching your repos from a local folder of your computer. It is still in testing.
>>
- `gites lpull`
    - Bulk pulling your repos from a local folder of your computer. It is still in testing.
>>

---

## The journey of using this package

### Step 1: Installation

Install Gites using pip:

```bash
pip install gites
```

### Step 2: Create a my_gites.json Configuration File

- To use gites effectively, you need to create a configuration file named `my_gites.json`. This file will store information about your repositories and their locations. Follow these guidelines:

- Ensure you place my_gites.json in a folder that's regularly backed up in the cloud, such as a local GitHub repository or Google Drive folder.

- Here's a template for `my_gites.json`:
    - "repositories": List your repositories here. Include the repository name and its remote URL (e.g., GitHub URL).
    - "root_directory": Specify the local directory where your repositories are stored on your computer.
```javascript
{
    "repositories": [
        {
            "name": "gites",
            "remote_url": "https://github.com/pakkinlau/gites"
        },

    ],
    "root_directory": "/home/kin/All_Github_Repos"
}


```
### Step 3: Use any `gites` commands from the terminal

Now that you've set up gites, you can start using it to manage your repositories efficiently. Simply open your terminal and execute Gites commands.

For example, to push all repositories from your local folder, run:
```bash
gites lpush
```
The first time you install or reinstall Gites, it will prompt you to specify the location of your `my_gites.json` datastore file. You can paste the file path of the file we have made in step 2, into the terminal.

![Alt text](images/setup demo.png)

Once you've set the configuration file's location, Gites won't ask for it again.

And the command will be automatically run

## Future development

1. Consider varying needs from the diversity of potential users. Adding / editing the package to provide more methods.
Such as: 
- Renaming a repo. `RenameManager()`
- Hard resolve conflicts for a repo (one-side overwrite): When remote and local is not consistent. Delete either one and then overwrite. 

2. Documentation: Use sphinx and readthedoc to produce an effective documentation to the user. Highlight, screenshot the features of the package as an image, or a video.

3. Improves the work summary message output from the package. 

## Contributing

Contributions to this repository are highly encouraged! If you have ideas for improvements, additional functionalities, or bug fixes, feel free to open an issue or submit a pull request. Let's collaborate to make Git management even more powerful and user-friendly.

## License

This repository is open-source and available under the [MIT License](LICENSE). You are welcome to use, modify, and distribute the code as per the terms of the license.

Enjoy using the Git-management package! 🚀
