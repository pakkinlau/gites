""" 
Test module:

How to run it?

- Click "run" would fails. 
When you run a Python script directly, Python doesn't set up the package context that's necessary for relative imports to work.

- To run your test, you should use `-m` flag with unittest. 
This approach keep the folder structure intact 

"""


import unittest
from unittest.mock import MagicMock, patch
from ..subpackage.datastore_json_handler import DatastoreJSONHandler

class TestConfigJSONHandler:
    # Mock of the ConfigJSONHandler class
    gites_datastore_json_location = "/mock/datastore.json"

class TestDatastoreJSONHandler(unittest.TestCase):
    def setUp(self):
        # Patch the ConfigJSONHandler to return a mock instance
        patcher = patch('datastore_json_handler.ConfigJSONHandler', new=TestConfigJSONHandler)
        self.mock_config = patcher.start()
        self.addCleanup(patcher.stop)
        
        # Mock data to be used in tests
        self.mock_datastore_data = {
            "repositories": [
                {"name": "repo1", "remote_url": "https://example.com/repo1.git"},
                {"name": "repo2", "remote_url": "https://example.com/repo2.git"}
            ],
            "root_directories": {
                "linux": "/linux/root",
                "windows": "C:\\windows\\root"
            }
        }

    def test_load_datastore_json(self):
        # Mock os.path.exists to always return True
        with patch('os.path.exists', return_value=True):
            # Mock the builtin open function to mock the file reading
            with patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps(self.mock_datastore_data))):
                handler = DatastoreJSONHandler()
                # Assert that the data is loaded correctly
                self.assertEqual(handler.data, self.mock_datastore_data)

    def test_get_root_directory_linux(self):
        # Set the os.name to 'posix' to simulate a Linux environment
        with patch('os.name', 'posix'):
            handler = DatastoreJSONHandler()
            # Assert that the Linux root directory is returned
            self.assertEqual(handler.get_root_directory(), "/linux/root")

    def test_get_root_directory_windows(self):
        # Set the os.name to 'nt' to simulate a Windows environment
        with patch('os.name', 'nt'):
            handler = DatastoreJSONHandler()
            # Assert that the Windows root directory is returned
            self.assertEqual(handler.get_root_directory(), "C:\\windows\\root")

    # Add more tests here to cover different scenarios and edge cases

if __name__ == '__main__':
    unittest.main()