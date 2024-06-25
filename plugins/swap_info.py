import json
from utils import run_command
from plugins.plugin import Plugin


class SwapInfoPlugin(Plugin):
    def __init__(self):
        super().__init__(plugin_id="swap_info")
        self.state_value = "active"

    def get_swap_status(self, json_output: bool = False) -> str:
        command = ['swapon', '--show']
        result = run_command(command)
        if not result["stdout"]:
            result["stdout"] = "No swap space configured."

        try:
            with open('/etc/security/swapshred.conf', 'r') as file:
                config_content = file.read().strip()
        except FileNotFoundError:
            config_content = "swapshred.conf not found."

        if json_output:
            return json.dumps(
                {'swap_status': result["stdout"], 'swapshred_config': config_content, 'error': result["stderr"]},
                indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Swap Status:\n{result['stdout']}\n\nSwapshred Configuration:\n{config_content}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def get_swap_usage(self, json_output: bool = False) -> str:
        command = ['free', '-h']
        result = run_command(command)
        if json_output:
            return json.dumps({'swap_usage': result["stdout"], 'error': result["stderr"]}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Swap Usage:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def status(self, directory:str = None, json_output: bool = False) -> str:
        return self.get_swap_status(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.get_swap_usage(json_output)

    def id(self) -> str:
        return self.plugin_id

    def state(self) -> str:
        return self.state_value
