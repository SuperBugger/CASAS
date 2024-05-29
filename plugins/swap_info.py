import subprocess
import json
from typing import Dict, Union


class Plugin:
    SZI_NAME = "swap_info"

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

    def get_swap_info(self, json_output: bool = False) -> str:
        command = ['swapon', '--show']
        result = self.run_command(command)
        if not result["stdout"]:
            result["stdout"] = "No swap space configured."
        if json_output:
            return json.dumps({'swap_info': result["stdout"], 'error': result["stderr"]}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Swap Information:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def get_swap_usage(self, json_output: bool = False) -> str:
        command = ['free', '-h']
        result = self.run_command(command)
        if json_output:
            return json.dumps({'swap_usage': result["stdout"], 'error': result["stderr"]}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Swap Usage:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def status(self, json_output: bool = False) -> str:
        return self.get_swap_info(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.get_swap_usage(json_output)
