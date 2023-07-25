import os

def print_folder_structure(folder_path, level=0, num_files_to_print=-1):
    # Get the files and directories in the current directory
    items = os.listdir(folder_path)

    # Loop through the items in the directory
    for i, item in enumerate(sorted(items)):
        # Determine the path of the item
        item_path = os.path.join(folder_path, item)

        # Print the item with appropriate indentation
        if os.path.isfile(item_path):
            if num_files_to_print < 0 or i < num_files_to_print:
                print(" " * level * 4 + "- " + item)
            elif i == num_files_to_print:
                print(" " * level * 4 + "- ...")
        else:
            print(" " * level * 4 + "- " + item)

        # Recursively print the contents of subfolders
        if os.path.isdir(item_path):
            print_folder_structure(item_path, level + 1, num_files_to_print)

# Replace 'PATH/TO/VAULT' with the path to your Obsidian vault
path = r"D:\All_programming_projects\Textual notes\Machine learning"
print_folder_structure(path,num_files_to_print=2)