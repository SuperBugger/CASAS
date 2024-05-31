import json
from utils import run_command


class Plugin:
    SZI_NAME = "integrity_check"

    def get_integrity_status(self, json_output: bool = False) -> str:
        command = ['md5deep', '-r', '/home/ivandor/Programs']  #todo: реализовать выбор директории
        result = run_command(command)
        if json_output:
            return json.dumps({'integrity_status': result["stdout"], 'error': result["stderr"]}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Integrity Check Status:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def get_integrity_info(self, json_output: bool = False) -> str:
        command = ['md5deep', '--version']
        result = run_command(command)
        if json_output:
            return json.dumps({'integrity_info': result["stdout"], 'error': result["stderr"]}, indent=4, ensure_ascii=False)
        else:
            formatted_output = f"Integrity Check Information:\n{result['stdout']}\n"
            if result["stderr"]:
                formatted_output += f"Error:\n{result['stderr']}\n"
            return formatted_output

    def status(self, json_output: bool = False) -> str:
        return self.get_integrity_status(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.get_integrity_info(json_output)
