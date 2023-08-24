"""
This is a private module that encapsulate the communication process from the JSONUpdater. 
This module should not contains main functions that the package would use. 
"""

import os
import json

## Default values: 
json_name = "pgf-config.json"

def get_default_userdata_path(json_name):
    if os.name == 'nt':  # Windows
        appdata_path = os.environ.get('APPDATA', os.path.expanduser('~'))
        path = os.path.join(appdata_path, 'YourApp')
    elif os.name == 'posix':  # Linux and macOS
        home_path = os.environ.get('HOME', os.path.expanduser('~'))
        path = os.path.join(home_path, '.yourapp')
    else:
        raise RuntimeError("Unsupported operating system")

    # Create the directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.join(path, json_name)

# this is just a default location. 
default_json_path = get_default_userdata_path(json_name)

# A concise interface function to other module:
def _load_json(json_file_path = default_json_path):
    json_existing_data = _JSONHandler(json_file_path)._load_json()
    return json_existing_data

def _write_json(data, json_file_path = default_json_path):
    _JSONHandler(json_file_path)._write_json(data)


### Complete structure: 
class _JSONHandler:
    def __init__(self, json_file_path= default_json_path):
        self.json_file_path = json_file_path

    def _load_json(self):
        existing_data = {}

        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, "r") as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON: {e}")

        if not isinstance(existing_data, dict):
            existing_data = {}

        if "repositories" not in existing_data:
            existing_data["repositories"] = []

        return existing_data

    def _write_json(self, data):
        try:
            with open(self.json_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print(f"JSON file updated successfully. For the details, visit the exact JSON file: {self.json_file_path}")
        except IOError as e:
            print(f"Error writing to JSON file: {e}")
            raise SystemExit("Terminating due to error writing to JSON file")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise SystemExit("Terminating due to unexpected error")

# Testing unit: 
if __name__ == "__main__":
    # this module need an existing json, or existing data, to perform action. 
    json_existing_data = _JSONHandler(default_json_path)
