import subprocess
import tkinter as tk

# Define the function that runs the script
def run_script():
    # Get the user inputs
    folder_location = folder_entry.get()
    repo_url = url_entry.get()

    # Update the global variable with the folder location
    global full_folder_location
    full_folder_location = folder_location

    # Construct the commands
    command1 = f"git init"
    command2 = f"git checkout -b main"
    command3 = f"git remote add origin {repo_url}"
    command4 = f"git config --global core.autocrlf false"

    command5 = f"git lfs install"
    command6 = f"git lfs track '*.zip' + ' *.tar.gz' + ' *.mp4' + ' *.pdf'"

    commit = "first commit"
    command7 = "git add --all"
    command8 = f'git commit -m "{commit}"'
    command9 = f"git push -u origin main"

    # Define the function that runs a single command
    def run_command(command):
        print(f"Run: {command}")
        subprocess.run(command, shell=True, cwd=full_folder_location)

    # Run each command one at a time
    run_command(command1)
    run_command(command2)
    run_command(command3)
    run_command(command4)
    run_command(command5)
    run_command(command6)
    run_command(command7)
    run_command(command8)
    run_command(command9)
    

# Create the GUI application
root = tk.Tk()
root.title("Create GitHub Repo")
root.geometry("400x200")

# Create the input fields and labels
folder_label = tk.Label(root, text="Folder Location:")
folder_label.pack()
folder_entry = tk.Entry(root)
folder_entry.pack()

url_label = tk.Label(root, text="Repository URL:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

# Create the button to run the script
run_button = tk.Button(root, text="Create Repository", command=run_script)
run_button.pack()

root.mainloop()