"""
This is a private module that encapsulate the communication process from the JSONUpdater. 
This module should not contains main functions that the package would use. 
"""

import os
import json
from .config_json_handler import ConfigJSONHandler

### Complete structure: 
class DatastoreJSONHandler:
    def __init__(self):
        self.config_json_handler = ConfigJSONHandler()
        # the following are the data from the datastore json: 
        self.gites_datastore_json_location = self.config_json_handler.gites_datastore_json_location # this is for naming convention.
        self.data = self.load_datastore_json()
        self.list_of_repo_details = self.data["repositories"] # this return a list of dictionary, containing 'name' and 'remote_url' key for each repo.
        self.root_dir = self.get_root_directory()

    def get_root_directory(self):
        # Determine the appropriate root directory based on the operating system
        if os.name == 'posix':  # Unix/Linux/Mac OS
            return self.data["root_directories"]["linux"]
        elif os.name == 'nt':  # Windows
            return self.data["root_directories"]["windows"]
        else:
            raise OSError("Unsupported operating system")

    def load_datastore_json(self):
        existing_data = {}

        # case 1: that location has exactly-matched file
        if os.path.exists(self.gites_datastore_json_location):
            with open(self.gites_datastore_json_location, "r") as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON: {e}")
        else:
            raise SystemExit(f"Terminating due to the datastore json file is not existing in: {self.gites_datastore_json_location}")
        # case 2a: after opening the file, the outermost structure is not a json
        if not isinstance(existing_data, dict):
            print("Please check the file. The whole file is not detected as a json file.")
            raise SystemExit("Terminating due to unexpected error")
        # case 2b: Check each item in the "repositories" data to verify it is well-structured. 
        for repo_detail in existing_data["repositories"]:
            if not isinstance(repo_detail, dict):
                print("Please check the file. The repository list of the file is not detected as a json file.")
                raise SystemExit("Terminating due to unexpected error")
        # case 3: after knowing it is a json, but the json has empty repo entries
        if "repositories" not in existing_data:
            print("it is an empty json. creating structure for it...")
            existing_data["repositories"] = []
        # case 4: if "root_directory" is not specified in the datastore json.
        if "root_directories" not in existing_data:
            raise SystemExit(f"Terminating due to the root directory of your git repository folders are not properly defined in your datastore json: {self.gites_datastore_json_location}")
        # finally return data
        return existing_data

# Testing unit: 
if __name__ == "__main__":
    # this module need an existing json, or existing data, to perform action. 
    # default_json_path = DatastoreLocationChecker().load_setup_json_and_get_datastore_json_address()
    # json_existing_data = _JSONHandler(default_json_path)
    # root_dir = json_existing_data.data.get("root_directory")
    # this is just a default location. 
    pass