import subprocess
import json


class Plugin:
    SZI_NAME = "antivirus_policy"

    def get_antivirus_info(self):
        try:
            result = subprocess.run(['clamscan', '--version'], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return "ClamAV antivirus utility not found."

    def status(self):
        antivirus_info = self.get_antivirus_info()
        return f"Antivirus information status: {antivirus_info}"

    def info(self):
        antivirus_info = self.get_antivirus_info()
        return self._format_output(antivirus_info)

    def _format_output(self, data, json_output=False):
        if json_output:
            return json.dumps({'antivirus_info': data}, indent=4)
        else:
            return f"Antivirus information: {data}"
