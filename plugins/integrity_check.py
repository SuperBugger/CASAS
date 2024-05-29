import subprocess
import json
from typing import Dict, Union


class Plugin:
    SZI_NAME = "integrity_check"

    def run_command(self, command: list) -> Dict[str, str]:
        result = {"stdout": "", "stderr": ""}
        try:
            process = subprocess.run(command, capture_output=True, text=True, check=True)
            result["stdout"] = process.stdout.strip()
            result["stderr"] = process.stderr.strip()
        except FileNotFoundError:
            result["stderr"] = f"{command[0]} utility not found."
        except subprocess.CalledProcessError as e:
            result["stderr"] = f"Error occurred while running {' '.join(command)}: {str(e)}"
        return result

    def get_integrity_status(self, json_output: bool = False) -> str:
        command = ['md5deep', '-r', '/home/ivandor/Programs']  #todo add the ability to select a directory
        result = self.run_command(command)
        if json_output:
            return json.dumps({'integrity_status': result["stdout"], 'error': result["stderr"]}, indent=4,
                              ensure_ascii=False)
        else:
            formatted_output = f"Integrity Check Status:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def get_integrity_info(self, json_output: bool = False) -> str:
        command = ['md5deep', '-version']
        result = self.run_command(command)
        if json_output:
            return json.dumps({'integrity_info': result["stdout"], 'error': result["stderr"]}, indent=4,
                              ensure_ascii=False)
        else:
            formatted_output = f"Integrity Check Information:\nMd5deep version: {result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def status(self, json_output: bool = False) -> str:
        return self.get_integrity_status(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.get_integrity_info(json_output)
