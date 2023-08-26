"""
This is a private module that encapsulate the communication process from the JSONUpdater. 
This module should not contains main functions that the package would use. 
"""

import os
import json
from subpackage.ConfigJSONHandler import ConfigJSONHandler



def load_datastore_json():
    datastore_full_path = DatastoreLocationChecker.get_full_path_of_datastore_json()

    if os.path.exists(datastore_full_path):
        
        with open(datastore_full_path, "r") as json_file:
            try:
                existing_data = json.load(json_file)
                return existing_data
            except json.JSONDecodeError as e:
                print(f"Error loading JSON: {e}")
    if not isinstance(existing_data, dict):
        print("it is pointing to a non-dictionary object")
        existing_data = {}
    if "repositories" not in existing_data:
        print("it is an empty json. creating structure for it...")
        existing_data["repositories"] = []
    return existing_data

def write_datastore_json():
    # load the whole json into a variable. Then edit the variable. Then write the json.
    datastore_full_path = DatastoreLocationChecker.get_full_path_of_datastore_json()
    data_of_datastore_json = load_datastore_json()
    try:
        with open(datastore_full_path, "w") as json_file:
            json.dump(self.data, json_file, indent=4)
        print(f"JSON file updated successfully. For the details, visit the exact JSON file: {self.json_file_path}")
    except IOError as e:
        print(f"Error writing to JSON file: {e}")
        raise SystemExit("Terminating due to error writing to JSON file")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise SystemExit("Terminating due to unexpected error")


### Complete structure: 
class _JSONHandler:
    def __init__(self):
        self.config_json_handler = ConfigJSONHandler()
        # the following are the data from the datastore json: 
        self.gites_datastore_json_location = self.config_json_handler.gites_datastore_json_location
        self.data = self.load_datastore_json()
        self.list_of_repo_details = self.data["repositories"]
        self.root_dir = self.data["root_directory"]

    def load_datastore_json(self):
        existing_data = {}

        # case 1: that location has exactly-matched file
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, "r") as json_file:
                try:
                    existing_data = json.load(json_file)
                    return existing_data
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON: {e}")
        # case 2: after opening the file, it is not a json
        if not isinstance(existing_data, dict):
            print("it is pointing to a non-dictionary object")
            existing_data = {}
        # case 3: after knowing it is a json, but the json has empty repo entries
        if "repositories" not in existing_data:
            print("it is an empty json. creating structure for it...")
            existing_data["repositories"] = []

        return existing_data

    def write_current_data_into_json(self):
        data_var = self.data
        if data_var is not None:
            try:
                with open(self.gites_datastore_json_location, 'w') as json_file:
                    json.dump(data_var, json_file, indent=4)
                print(f"Datastore json updated.")
            except Exception as e:
                print(f"An error occurred: {e}")


    def update_root_dir(self,new_root_dir):
        self.data["root_directory"] = new_root_dir
        self.write_current_data_into_json()

# Testing unit: 
if __name__ == "__main__":
    # this module need an existing json, or existing data, to perform action. 
    default_json_path = DatastoreLocationChecker().load_setup_json_and_get_datastore_json_address()
    json_existing_data = _JSONHandler(default_json_path)
    root_dir = json_existing_data.data.get("root_directory")
    # this is just a default location. 

    print(root_dir)


# A concise interface function to other module:
def _load_json(json_file_path = default_json_path):
    json_existing_data = _JSONHandler(json_file_path)._load_json()
    return json_existing_data

def _write_json(data, json_file_path = default_json_path):
    _JSONHandler(json_file_path)._write_json(data)

