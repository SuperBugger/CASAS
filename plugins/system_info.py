import platform
import json
from typing import Dict
from utils import run_command


class Plugin:
    SZI_NAME = "system_info"

    def get_system_info(self) -> Dict[str, str]:
        system_info = {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
        return system_info

    def get_system_status(self, json_output: bool = False) -> str:
        command = ['uptime']
        result = run_command(command)
        if json_output:
            return json.dumps({'system_status': result["stdout"], 'error': result["stderr"]}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"System Status:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def get_system_details(self, json_output: bool = False) -> str:
        system_info = self.get_system_info()
        if json_output:
            return json.dumps({'system_details': system_info}, indent=4, ensure_ascii=False)
        else:
            formatted_output = "System Information Details:\n"
            for key, value in system_info.items():
                formatted_output += f"{key.capitalize()}: {value}\n"
            return formatted_output

    def status(self, json_output: bool = False) -> str:
        return self.get_system_status(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.get_system_details(json_output)
