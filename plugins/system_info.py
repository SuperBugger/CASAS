import platform
import json


class Plugin:
    SZI_NAME = "system_info"

    def get_system_info(self):
        system_info = {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
        return system_info

    def status(self):
        system_info = self.get_system_info()
        return f"System information status: {system_info}"

    def info(self):
        system_info = self.get_system_info()
        return self._format_output(system_info)

    def _format_output(self, data, json_output=False):
        if json_output:
            return json.dumps({'system_info': data}, indent=4)
        else:
            formatted_output = ''
            for key, value in data.items():
                formatted_output += f"{key.capitalize()}: {value}\n"
            return formatted_output
