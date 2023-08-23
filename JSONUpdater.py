"""
The package aims to help user to curate a configuration json that holds all hard-data needed to process the workflow.  

There should be 2 exact-copies of `pgf-config.json` stored in different locations.
- One is putting within the package. This copy allow the package run smoothly without having nuance setup.
- Another one is putting in a customized location. This copy allow the user backup the config avoiding loss of data incidently. (eg when they upgrade the package. )
"""

import os
import json
from JSONHandler import JSONHandler

default_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pgf-config.json")

class JSONUpdater:
    def __init__(self, script_directory, json_file_path):
        self.script_directory = script_directory # reserve it for future development
        self.json_handler = JSONHandler(json_file_path)
        self.existing_data = self.json_handler.load_data()

    def update_root_directory(self, root_directory):
        self.existing_data["root_directory"] = root_directory

    def find_remote_url_with_repo_name(self, repository_name):
        for repo in self.existing_data["repositories"]:
            if repo["name"] == repository_name:
                return repo["remote_url"]
        return None

    def update_repo_info(self, list_of_repo):
        existing_repo_names = {repo["name"] for repo in self.existing_data["repositories"]}
        created_record = []
        rewrited_record = []
        unchanged_record = []

        for repo_name, repo_url in list_of_repo.items():
            if repo_name in existing_repo_names:
                existing_url = self.find_remote_url_with_repo_name(repo_name)
                if repo_url == existing_url:
                    unchanged_record.append(repo_name)
                    continue
                else:
                    for repo_record in self.existing_data["repositories"]:
                        if repo_record["name"] == repo_name:
                            repo_record["remote_url"] = repo_url
                            rewrited_record.append(repo_name)
                            break
            else:
                self.existing_data["repositories"].append({"name": repo_name, "remote_url": repo_url})
                created_record.append(repo_name)

        self.json_handler.write_data(self.existing_data)
        self.print_summary(created_record, rewrited_record, unchanged_record)

    def print_summary(self, created_record, rewrited_record, unchanged_record):
        print(f"Created records: {created_record}")
        print(f"Rewritten records: {rewrited_record}")
        print(f"Unchanged records: {unchanged_record}")


# Testing unit: 
if __name__ == "__main__":
    
    root_directory = os.path.join(os.path.expanduser("~"), "All_Github_Repos")
    list_of_repo = {
        # "Git management": "https://github.com/pakkinlau/your-repo.git", # A repo should not clone itself. 
        "Guides": "https://github.com/pakkinlau/guides.git",
        "Textual notes": "https://github.com/pakkinlau/textual-notes.git",
        "Tutorial template": "https://github.com/pakkinlau/tutorial-template.git",
        "Video materials": "https://github.com/pakkinlau/video-materials.git",
        "JS webpage coding gym": "https://github.com/pakkinlau/js-webpage-coding-gym.git",
        "Python coding gym": "https://github.com/pakkinlau/python-coding-gym.git",
    }

    # Determine the path to the JSON file in the same directory as the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_directory, "pgf-config.json")

    json_updater = JSONUpdater(script_directory, json_file_path)
    json_updater.update_root_directory(root_directory)
    json_updater.update_repo_info(list_of_repo)