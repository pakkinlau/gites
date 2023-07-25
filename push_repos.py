import os
import os
import  util

# Use this when choosing "All programming projects" as root folder.
root_folder = r"D:\All_programming_projects"
os.chdir(root_folder)

"""
list_of_repo = [
    "Git management",
    "Guides",
    "Python coding gym",
    "Textual notes",
    "Tutorial template",
    "Video materials",
    "JS webpage coding gym"
]
"""
list_of_repo = [
    "Large file storage test"
]



repo_list = [f".\{elt}" for elt in list_of_repo]

util.listpush(repo_list)

    