import datetime
import json
import subprocess
from abc import ABC

from plugins.plugin import Plugin


class PasswordPolicyPlugin(Plugin, ABC):
    def __init__(self):
        super().__init__(plugin_id="password_policy")
        self.state_value = "active"

    def read_passwd_file(self, json_output: bool = False) -> str:
        try:
            with open('/etc/passwd', 'r') as file:
                passwd_content = file.readlines()
        except FileNotFoundError:
            passwd_content = []

        parsed_passwd = [line.strip().split(':') for line in passwd_content]
        passwd_info = [{"username": entry[0], "uid": entry[2], "gid": entry[3], "home": entry[5], "shell": entry[6]} for
                       entry in parsed_passwd]

        if json_output:
            return json.dumps({'passwd_info': passwd_info}, indent=4, ensure_ascii=False)
        else:
            formatted_output = "Parsed /etc/passwd Content:\n"
            for entry in passwd_info:
                formatted_output += f"Username: {entry['username']}, UID: {entry['uid']}, GID: {entry['gid']}, Home: {entry['home']}, Shell: {entry['shell']}\n"
            return formatted_output

    def get_password_policy_status(self, json_output: bool = False) -> str:
        expiry_results = subprocess.run(['chage', '-l'], capture_output=True, text=True)
        expiry_info = expiry_results.stdout.strip().split('\n') if expiry_results.stdout else []

        last_change_results = []
        empty_password_users = []
        with open('/etc/shadow', 'r') as file:
            for line in file:
                parts = line.split(':')
                if len(parts) > 2:
                    username = parts[0]
                    last_change = parts[2]
                    if last_change.isdigit():
                        last_change_date = datetime.datetime.fromtimestamp(int(last_change) * 86400).strftime(
                            '%Y-%m-%d')
                        last_change_results.append(f"{username}: {last_change_date}")
                    if parts[1] == '' or parts[1] == '*':
                        empty_password_users.append(username)

        status_info = {
            "password_expiry": expiry_info,
            "password_last_change": last_change_results,
            "empty_password_users": empty_password_users
        }

        if json_output:
            return json.dumps(status_info, indent=4, ensure_ascii=False)
        else:
            formatted_output = "Password Expiry Information:\n" + "\n".join(expiry_info) + "\n\n"
            formatted_output += "Password Last Change Information:\n" + "\n".join(last_change_results) + "\n\n"
            formatted_output += "Users with Empty Passwords:\n" + "\n".join(empty_password_users) + "\n"
            return formatted_output

    def status(self, directory: str = None, json_output: bool = False) -> str:
        return self.get_password_policy_status(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.read_passwd_file(json_output)

    def id(self) -> str:
        return self.plugin_id

    def state(self) -> str:
        return self.state_value
