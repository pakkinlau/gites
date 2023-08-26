import os
import json

# interface functions


# A good class should store its resources in its attribute, not getting them every time in the running process. 
# That's very good to "keep things into record, as an attribute. " Especially for the process that could be completed immediately. 
# This class should not depend on other classes / functioos 
class ConfigJSONHandler:

    def __init__(self):
        # all details of config.json should be put at here. 
        self.config_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "package_setup.json")
        self.config_data = self.load_config()
        self.json_initial_setup_check = self.config_data["initial_setup"]
        self.default_datastore_json_name = self.config_data["default_datastore_json_name"]
        self.root_dir_of_gites_datastore_json = self.check_initial_setup_then_get_datastore_json_address()
        self.gites_datastore_json_location = os.path.join(self.root_dir_of_gites_datastore_json, self.default_datastore_json_name)

    def load_config(self):
        if os.path.exists(self.config_json_path):
            with open(self.config_json_path, "r") as json_file:
                return json.load(json_file)
        else:
            print("Config JSON file not found:", self.config_json_path)
            return None

    def update_config(self, key, value):
        """Update the value for a specific key in the config.json."""
        config = self.config_data
        if config is not None:
            try:
                config[key] = value
                with open(self.config_json_path, 'w') as json_file:
                    json.dump(config, json_file, indent=4)
                print(f"Updated '{key}' with '{value}' in '{self.config_json_path}'.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def check_initial_setup_then_get_datastore_json_address(self):
        default_datastore_json_name = self.default_datastore_json_name
        default_json_path = self.get_default_userdata_path(default_datastore_json_name)

        prompt = f"""
        You are the first time using the package, or have upgraded the package. 
        If you want to define a customized my_gites.json in the next step, enter y.
        If you want to use the default location, enter n.
        (Default location: {default_json_path})
        
        Please enter (y/n) to proceed.
        """

        if not self.json_initial_setup_check:
            return self.config_data["gites_datastore_json_location"]
        else:
            use_custom_path = input(prompt)
            if use_custom_path.lower() == "y":
                custom_path = input(f"Please enter the directory address that contains your {default_datastore_json_name}. "
                                    f"The example is '/home/kin/.yourapp/'. Please do not include the file name. ")
                self.update_config("gites_datastore_json_location", custom_path)
                self.update_config("initial_setup", False)
                return custom_path
            elif use_custom_path.lower() == "n":
                self.update_config("gites_datastore_json_location", default_json_path)
                self.update_config("initial_setup", False)
                return default_json_path
            else:
                print("Invalid input.")
                raise SystemExit("Exiting due to invalid input.")

    def get_default_userdata_path(self, json_name):
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

if __name__ == "__main__":
    datastore_address = ConfigJSONHandler().gites_datastore_json_location