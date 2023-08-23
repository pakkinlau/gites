import os
import json

default_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pgf-config.json")

class JSONHandler:
    def __init__(self, json_file_path= default_json_path):
        self.json_file_path = json_file_path

    def load_data(self):
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

    def write_data(self, data):
        with open(self.json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON file updated successfully. For the details, visit the exact JSON file: {self.json_file_path}")

# Testing unit: 
if __name__ == "__main__":
    json_existing_data = JSONHandler(default_json_path)