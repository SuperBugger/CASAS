import subprocess
import json
from typing import Dict, Union


class Plugin:
    SZI_NAME = "firewall_policy"

    def run_command(self, command: list) -> str:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
        except FileNotFoundError:
            output = f"{command[0]} utility not found."
        except subprocess.CalledProcessError as e:
            output = f"Error occurred while running {' '.join(command)}: {str(e)}"
        return output

    def get_firewall_status(self) -> str:
        command = ['systemctl', 'status', 'ufw']
        return self.run_command(command)

    def get_firewall_info(self) -> str:
        command = ['ufw', 'status', 'verbose']
        return self.run_command(command)

    def status(self, json_output: bool = False) -> str:
        firewall_status = self.get_firewall_status()
        if json_output:
            return json.dumps({'status': firewall_status}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Status:\n{firewall_status}\n"
            return formatted_output

    def info(self, json_output: bool = False) -> str:
        firewall_info = self.get_firewall_info()
        if json_output:
            return json.dumps({'info': firewall_info}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Info:\n{firewall_info}\n"
            return formatted_output

