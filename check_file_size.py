import os
import util

folder_path = r"D:\All_programming_projects" 

# ======

if __name__ == "__main__":
    gt_100mb_list = util.get_files_bigger_than_100mb(folder_path)
    print(gt_100mb_list)