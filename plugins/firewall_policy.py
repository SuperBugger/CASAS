import subprocess
import json


class Plugin:
    SZI_NAME = "firewall_policy"

    def get_firewall_status(self):
        try:
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return "UFW (Uncomplicated Firewall) utility not found."
        except subprocess.CalledProcessError as e:
            return f"Error getting firewall status: {e}"

    def get_firewall_rules(self):
        try:
            result = subprocess.run(['ufw', 'status', 'verbose'], capture_output=True, text=True)
            return result.stdout.strip()
        except FileNotFoundError:
            return "UFW (Uncomplicated Firewall) utility not found."
        except subprocess.CalledProcessError as e:
            return f"Error getting firewall rules: {e}"

    def status(self):
        firewall_status = self.get_firewall_status()
        return self._format_output({'status': firewall_status})

    def info(self):
        firewall_rules = self.get_firewall_rules()
        return self._format_output({'rules': firewall_rules})

    def _format_output(self, data, json_output=False):
        if json_output:
            return json.dumps(data, indent=4)
        else:
            formatted_output = ''
            for key, value in data.items():
                formatted_output += f"{key.capitalize()}:\n{value}\n"
            return formatted_output
