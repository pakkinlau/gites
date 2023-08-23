import os
import subprocess

# A concise interface function to other module:  
def run(cmd: str, loc: str) -> tuple[int, str]:
    return_code, stdout = SubprocessHandler(cmd, loc).run()
    return return_code, stdout

# Complete structure: 
class SubprocessHandler:
    def __init__(self, command, location):
        self.command = command
        self.location = location
    
    def run(self):
        """This method runs a command and captures its output and return code."""
        print("=" * 30)
        print(f"Working in the {os.path.abspath(self.location)} folder...")
        print(f"Run: {self.command}")
        
        # there are 3 possible cases: Successful-non-zero, successful-zero, Failed-subprocess. 
        try:
            # This version of subprocess.Popen() could return all message from execution process. 
            result = subprocess.Popen(
                self.command,
                cwd=self.location,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Capture the standard output and standard error
            stdout, stderr = result.communicate()
            string_stdout = stdout.decode('utf-8')
            string_stderr = stderr.decode('utf-8')
            return_code = result.returncode
            
            # In the current setting, print all outputs from terminal for development purpsoe 
            print("Returned exit code:", return_code)
            if not string_stdout:
                print("Standard Output: <--- It is empty!")
            else:
                print("Standard Output:", string_stdout)
            if not string_stderr:
                print("Standard Error: <--- It is empty!")
            else:
                print("Standard Error:", string_stderr)
            
            # Case 2: Successful-zero
            if return_code == 0:
                print("Command executed successfully!")
            # Case 1: Successful-non-zero
            else:
                print("Command failed. Please check the above messages")
                
            return return_code, string_stdout
        # Case 3a: If there is any non-zero return code
        except subprocess.CalledProcessError as e:
            print("Subprocess failed with exit code:", e.returncode)
            print("Error output:", e.stderr)
        # Case 3b: Generic catch-all for any other exceptions. 
        except Exception as e:
            print("An error occurred:", e)

# Testing unit: 
if __name__ == "__main__":
    command_to_run = ["ls", "-l"]
    working_location = os.getcwd()
    handler = SubprocessHandler(command_to_run, working_location)
    handler.run()
    # return success in 23 Aug 2023