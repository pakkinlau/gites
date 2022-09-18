import util

list_of_repo = [
    "Early old works",
    "Git management",
    "Python coding gym",
    "Textual notes",
]

list_of_location = [f".\{elt}" for elt in list_of_repo]

for elt in list_of_location:
    util.push(elt)
    import subprocess
