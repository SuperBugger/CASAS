import subprocess
import json


class Plugin:
    SZI_NAME = "host_policy"

    def get_host_info(self):
        try:
            result = subprocess.run(['hostnamectl'], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return "hostnamectl utility not found."

    def status(self):
        host_info = self.get_host_info()
        return f"Host information status: {host_info}"

    def info(self):
        host_info = self.get_host_info()
        return self._format_output(host_info)

    def _format_output(self, data, json_output=False):
        if json_output:
            return json.dumps({'host_info': data}, indent=4)
        else:
            return f"Host information: {data}"
