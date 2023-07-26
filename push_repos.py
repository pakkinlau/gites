import os
import os
import util
import time

def main():
    start_time = time.time()

    # Use this when choosing "All programming projects" as root folder.
    root_folder = r"D:\All_programming_projects"
    os.chdir(root_folder)


    list_of_repo = [
        "Git management",
        "Guides",
        "Python coding gym",
        "Textual notes",
        "Tutorial template",
        "Video materials",
        "JS webpage coding gym"
    ]



    repo_list = [f".\{elt}" for elt in list_of_repo]

    # It is resource heavy. Don't use it in an old repo.
    """ 
    for repo in repo_list:
        list = util.get_files_bigger_than_100mb(repo)
        if len(list)>0:
            sys.exit()
        else:
            continue
    """

    util.listpush(repo_list)
    
    # Print the results
    end_time = time.time()
    time_spent = end_time - start_time
    print("Start Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
    print("End Time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
    print("Time Spent:", "{:.2f} seconds".format(time_spent))

if __name__ == "__main__":
    main()