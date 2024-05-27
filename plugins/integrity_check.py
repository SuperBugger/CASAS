import subprocess
import json


class Plugin:
    SZI_NAME = "integrity_check"

    def get_integrity_status(self):
        try:
            result = subprocess.run(['aide', '--check'], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return "AIDE (Advanced Intrusion Detection Environment) utility not found."
        except subprocess.CalledProcessError as e:
            return f"Error running integrity check: {e}"

    def status(self):
        integrity_status = self.get_integrity_status()
        return self._format_output({'integrity_status': integrity_status})

    def info(self):
        integrity_status = self.get_integrity_status()
        return self._format_output({'integrity_info': integrity_status})

    def _format_output(self, data, json_output=False):
        if json_output:
            return json.dumps(data, indent=4)
        else:
            formatted_output = ''
            for key, value in data.items():
                formatted_output += f"{key.capitalize().replace('_', ' ')}:\n{value}\n"
            return formatted_output
