-> Aug 23, 2023:
Add: `JSONHandler.py`, `JSONUpdater.py`
Changes: 
For details, check https://github.com/pakkinlau/Git-flow-master/compare/61acdee..0d88b8c

`GitPushManager.py`, 

-> Aug 21, 2023:
Changes: `util.py`, `push_repos.py`, `clone_my_own_repo.py`
For details, check https://github.com/pakkinlau/Git-flow-master/compare/cf4283d..61acdee

Compatibility fix:
- Fixed the compatibility problem when the package is used in LinuxOS/windowsOS. 

Subprocess:
- Considered the exit-code provided by git commands to improve the error-handling of the package. 

`clone_my_own_repo.py`:
- Adopted numerical value `0,1,2` in `status_message` as a message holder to describe each package is going to be cloned or not. 
- Added: post-download verification. After completion of cloning, verify the status of the repo
- Summary: Added 3 list to count which repos are whether cloned successfully/failed/nothing changed 

`push_repos.py`:
- OS-independent update: Use `os.path.join(os.path.expanduser("~"), "All_Github_Repos")` to represent root directory.
- Hard-code reduction: Let the script search for all repos that exist in the root footer, instead of requiring the user to write them one-by-one.

`util.py`:
- Subprocess capture: `result.communicate()` and `subprocess.Repon()`
- Adoption of git exit code: Which helps error-handling process. 
- Adoption of output string matching error handling: can write the `if` statement and compare the match of git outputs to complete the logic. 
- Rewrote the error-handling logic with keyword `continue`, `return` and exit code. 
- Broke down the compound `try`, `except` block into parallel individual blocks. 
- Mistane: Logging updates: Use `print("=" * 30)` for creating long lines reducing reduntancy
- Mistane: Imrpoved the documentation. Clearly highlight the cases. 


-> 21 Jul 2023:
- A Basic version that could be run in windows OS is released. 