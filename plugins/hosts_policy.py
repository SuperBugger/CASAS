import subprocess
import json
from typing import Dict, Union


class Plugin:
    SZI_NAME = "host_policy"

    def run_command(self, command: list) -> str:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
        except FileNotFoundError:
            output = f"{command[0]} utility not found."
        except subprocess.CalledProcessError as e:
            output = f"Error occurred while running {' '.join(command)}: {str(e)}"
        return output

    def get_host_status(self, json_output: bool = False) -> str:
        command = ['hostnamectl']
        host_status = self.run_command(command)
        if json_output:
            return json.dumps({'host_status': host_status}, indent=4, ensure_ascii=False)
        else:
            return host_status

    def get_host_info(self, json_output: bool = False) -> str:
        command = ['uname', '-a']
        host_info = self.run_command(command)
        if json_output:
            return json.dumps({'host_info': host_info}, indent=4, ensure_ascii=False)
        else:
            return host_info

    def status(self, json_output: bool = False) -> str:
        host_status = self.get_host_status(json_output)
        if json_output:
            return host_status
        else:
            formatted_output = f"Host Status:\n{host_status}\n"
            return formatted_output

    def info(self, json_output: bool = False) -> str:
        host_info = self.get_host_info(json_output)
        if json_output:
            return host_info
        else:
            formatted_output = f"Host Information:\n{host_info}\n"
            return formatted_output
