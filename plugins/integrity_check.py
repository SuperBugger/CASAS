import json
from plugins.plugin import Plugin
from utils import run_command


class IntegrityCheckPlugin(Plugin):
    def __init__(self):
        super().__init__(plugin_id="integrity_check")
        self.state_value = "active"

    def get_integrity_status(self, directory: str, json_output: bool = False) -> str:
        command = ['md5deep', '-r', directory]
        result = run_command(command)
        if json_output:
            return json.dumps({'integrity_status': result["stdout"], 'error': result["stderr"]}, indent=4,
                              ensure_ascii=False)
        else:
            formatted_output = f"Integrity Check Status for {directory}:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def get_integrity_info(self, json_output: bool = False) -> str:
        version_command = ['md5deep', '-version']
        which_command = ['which', 'md5deep']

        version_result = run_command(version_command)
        which_result = run_command(which_command)

        if json_output:
            return json.dumps({
                'integrity_version': version_result["stdout"],
                'md5deep_location': which_result["stdout"],
                'error': version_result["stderr"] + which_result["stderr"]
            }, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Md5deep version:\n{version_result['stdout']}\n"
            formatted_output += f"Md5deep Location:\n{which_result['stdout']}\n"
            if version_result["stderr"] or which_result["stderr"]:
                formatted_output += f"Error:\n{version_result['stderr']} {which_result['stderr']}\n"
            return formatted_output

    def status(self, directory: str = None, json_output: bool = False) -> str:
        if directory:
            return self.get_integrity_status(directory, json_output)
        else:
            return "No directory specified for integrity check."

    def info(self, json_output: bool = False) -> str:
        return self.get_integrity_info(json_output)

    def id(self) -> str:
        return self.plugin_id

    def state(self) -> str:
        return self.state_value
