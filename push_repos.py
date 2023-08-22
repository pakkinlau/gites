import os
import util
import time

def main():
    start_time = time.time()

    # locate to the root folder 
    root_folder = os.path.join(os.path.expanduser("~"), "All_Github_Repos")
    os.chdir(root_folder)

    # get all folders 
    all_items = os.listdir(root_folder)
    repo_list = [os.path.join(".", item) for item in all_items if os.path.isdir(os.path.join(root_folder, item)) and not item.startswith('.')]
    print(f"Totally there are {len(repo_list)} repos to work on. They are: {repo_list}")
    # The result would be : ['./Video materials', './Git management', './Textual notes', './Guides', './Tutorial template', './JS webpage coding gym', './Python coding gym', './Git-flow-master']

    util.listpush(repo_list)
    
    # Print the results
    end_time = time.time()
    time_spent = end_time - start_time
    print("Start Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
    print("End Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
    print("Time Spent:", "{:.2f} seconds".format(time_spent))

if __name__ == "__main__":
    main()

# This part tries to check all files size before 'util.listpush(repo_list)'. It is resource heavy. Don't use it in an old repo.
""" 
for repo in repo_list:
    list = util.get_files_bigger_than_100mb(repo)
    if len(list)>0:
        sys.exit()
    else:
        continue
"""

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
# Old way: repo_list = [os.path.join(".", elt) for elt in list_of_repo]
# In linux, the result would be a list of string: ['./Git management', './Guides', './Python coding gym', './Textual notes', './Tutorial template', './Video materials', './JS webpage coding gym']
"""