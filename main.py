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
    # Get the utils.py --- check the output lines done. 
    # Then copy the important lines, save it to 
