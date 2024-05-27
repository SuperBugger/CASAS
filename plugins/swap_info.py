import subprocess
import json

class Plugin:
    SZI_NAME = "swap_info"

    def get_swap_info(self):
        try:
            result = subprocess.run(['swapon', '--show'], capture_output=True, text=True)
            if result.stdout.strip():
                return result.stdout.strip()
            else:
                return "No swap space configured."
        except FileNotFoundError:
            return "swapon utility not found."
        except subprocess.CalledProcessError as e:
            return f"Error getting swap info: {e}"

    def get_swap_usage(self):
        try:
            result = subprocess.run(['free', '-h'], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return "free utility not found."
        except subprocess.CalledProcessError as e:
            return f"Error getting swap usage: {e}"

    def status(self):
        swap_info = self.get_swap_info()
        return self._format_output({'swap_info': swap_info})

    def info(self):
        swap_usage = self.get_swap_usage()
        return self._format_output({'swap_usage': swap_usage})

    def _format_output(self, data, json_output=False):
        if json_output:
            return json.dumps(data, indent=4)
        else:
            formatted_output = ''
            for key, value in data.items():
                formatted_output += f"{key.capitalize().replace('_', ' ')}:\n{value}\n"
            return formatted_output
