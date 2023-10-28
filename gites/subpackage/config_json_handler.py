import os
import json

"""
This module is writing a class "ConfigJSONHandler". 
This class's main functionality is the 'check_initial_setup_then_get_datastore_json_address()' method.
Which should be triggered when the user is the first time using the package, or the user just reinstalled the package. 

"""
"""
# Learning journey:

# A good class should store its resources in its attribute, 
# not getting them every time in the running process. 
# That's very good to "keep things into record, as an attribute.
# Especially for the process that could be completed immediately. 
# This class should not depend on other classes / functioos 


# To-do list:
1. Improve error handling - Done. 
2. Spacing: Some of your indentation and spacing inside the prompt strings could be improved for better readability.


"""

# interface functions



class ConfigJSONHandler:

    def __init__(self):
        # all details of config.json should be put at here. 
        self.config_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "package_setup.json")
        # return something like: /home/kin/All_Github_Repos/gites/gites/subpackage/package_setup.json
        self.config_data: dict = self._load_config()
        # the second parameter of `.get()` method is the value to be returned if the key is not found in the dictionary. 
        self.json_initial_setup_check = self.config_data.get("initial_setup", False) #
        self.default_datastore_json_name = self.config_data.get("default_datastore_json_name", "my_gites.json")
        self.root_dir_of_gites_datastore_json = self.check_initial_setup_then_get_datastore_json_address()
        self.gites_datastore_json_location = os.path.join(self.root_dir_of_gites_datastore_json, self.default_datastore_json_name)


    def _load_config(self):
        """A private method that loads config json of the package. 
        No inputs needed because the location of the config file is fixed. """
        if os.path.exists(self.config_json_path):
            try:
                with open(self.config_json_path, "r") as json_file:
                    return json.load(json_file) # 
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                raise SystemExit("Terminating due to unexpected error")
        else:
            print("Config JSON file not found:", self.config_json_path)
            raise RuntimeError(f"Failed to load config data on the location: {self.config_json_path}")

    def _update_config(self, key, value):
        """A private method that update values for a specific key on the config.json.
        The user need must specify which key, which value. 
        """
        config = self.config_data
        if config is not None:
            try:
                config[key] = value
                with open(self.config_json_path, 'w') as json_file:
                    json.dump(config, json_file, indent=4)
                print(f"Updated '{key}' with '{value}' in '{self.config_json_path}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
                raise SystemExit("Terminating due to unexpected error")

    def _get_default_userdata_path(self, json_name):
        """ This private tries to generate a "default location" for our datastore json. 
        "default location" is an option of 'check_initial_setup' when the user is asked whether
        they specify a location, or just use the default location. 
        
        The input variable 'json_name' is pre-defined in config json.
        """
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

    def check_initial_setup_then_get_datastore_json_address(self):
        """This is the main functionality of this class. When gites is initialized. This method should be called. 
        When the user is the first time using this package, or he just updated the package. 
        The user need to specify the location of the datastore json. 
        
        If the user didn't used this package before, this package will create a new datastore json for the user.
        """
        default_datastore_json_name = self.default_datastore_json_name
        default_json_path = self._get_default_userdata_path(default_datastore_json_name)

        prompt = f"""
        You are the first time using the package, or have upgraded the package. 
        If you want to define a customized path for your datastore json in the next step, enter y.
        If you want to use the default location, enter n.
        
        
        Please enter (y/n) to proceed.
        """

        # Case 1: If it is already not the first time using the package after (re)installing, 
        # skip all other process and just load the location from config.json. 
        if not self.json_initial_setup_check:
            return self.config_data["gites_datastore_json_location"]
        # Case 2: If it is the first time using the package. Guiding the user to complete the specification. 
        else:
            use_custom_path = input(prompt)
            if use_custom_path.lower() == "y":
                try:
                    custom_path = input(f"Please enter the directory address that contains your {default_datastore_json_name}. "
                                        f"The example is '/home/kin/.yourapp/'. Please do not include the file name. ")
                    if (custom_path.endswith("/") or custom_path.endswith("\\")):
                        raise SystemExit("Terminating the program since your specified directory path seems wrong. The format should be in like: '/home/kin/All_github_repos/Factual Value Asset'. Try the command and configure it again.")
                    else:
                        self._update_config("gites_datastore_json_location", custom_path)
                        self._update_config("initial_setup", False)
                        
                    return custom_path
                except Exception as e:
                    print(f"Error creating custom path: {e}")
                    raise SystemExit("Terminating due to unexpected error")
            elif use_custom_path.lower() == "n":
                message = f"Default location of your json file: {default_json_path}"
                input(message + " Press any key to continue...")
                self._update_config("gites_datastore_json_location", default_json_path)
                self._update_config("initial_setup", False)
                
                return default_json_path
            else:
                print("Invalid input.")
                raise SystemExit("Exiting due to invalid input.")

if __name__ == "__main__":
    datastore_address = ConfigJSONHandler().gites_datastore_json_location