import subprocess
import json
from typing import Dict, Union


class Plugin:
    SZI_NAME = "antivirus_policy"

    def run_command(self, commands: Dict[str, list], json_output: bool = False) -> str:
        results = {}
        for name, command in commands.items():
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                results[name] = result.stdout.strip()
            except FileNotFoundError:
                results[name] = f"{name} utility not found."
            except subprocess.CalledProcessError as e:
                results[name] = f"Error occurred while running {name}: {str(e)}"

        if json_output:
            return json.dumps(results, indent=4)
        else:
            formatted_info = "Antivirus Information:\n"
            for name, result in results.items():
                formatted_info += f"{name}: {result}\n"
            return formatted_info

    def get_antivirus_info(self, json_output: bool = False) -> str:
        antivirus_commands = {
            'ClamAV': ['clamscan', '--version'],
            'Sophos': ['savscan', '--version'],
            'ESET NOD32': ['esets_scan', '--version'],
            'Kaspersky': ['kav', '--version'],
            'Dr.Web': ['drwebd', '--version'],
        }
        return self.run_command(antivirus_commands, json_output)

    def get_antivirus_status(self, json_output: bool = False) -> str:
        antivirus_commands = {
            'ClamAV': ['clamscan', 'status'],
            'Sophos': ['savscan', 'status'],
            'ESET NOD32': ['esets_scan', 'status'],
            'Kaspersky': ['kav', 'status'],
            'Dr.Web': ['drwebd', 'status'],
        }
        return self.run_command(antivirus_commands, json_output)

    def status(self, json_output: bool = False) -> str:
        return self.get_antivirus_status(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.get_antivirus_info(json_output)

