import json
from datetime import datetime, timedelta
from plugins.plugin import Plugin


class AccountInfoPlugin(Plugin):
    uaDeletedPassword = 1
    uaBlockedPassword = 2
    uaTemporaryPassword = 4
    uaBlockedAccount = 8
    uaInvalidExpireDate = 16

    def __init__(self):
        super().__init__(plugin_id="account_info")
        self.state_value = "active"

    def analyze_user_info(self, user_info):
        expire_date = (datetime(1970, 1, 1) + timedelta(days=int(user_info[7]))) if user_info[7] != '' and int(
            user_info[7]) != -1 else None
        pwd_length = len(user_info[1])
        flags = 0

        if pwd_length == 0 or (pwd_length == 1 and user_info[1][0] == '!'):
            flags |= self.uaDeletedPassword

        if pwd_length > 0 and user_info[1][0] == '!':
            flags |= self.uaBlockedPassword

        if user_info[2] == '':
            flags |= self.uaTemporaryPassword

        if expire_date and expire_date < datetime.now():
            flags |= self.uaBlockedAccount

        try:
            if int(user_info[7]) == -1:
                flags |= self.uaInvalidExpireDate
        except ValueError:
            pass

        return flags

    def parse_shadow_file(self, shadow_file_path='/etc/shadow'):
        user_info = {}
        try:
            with open(shadow_file_path, 'r') as file:
                for line in file:
                    fields = line.strip().split(':')
                    username = fields[0]
                    user_info[username] = self.analyze_user_info(fields)
        except FileNotFoundError:
            print(f"File {shadow_file_path} not found.")
        return user_info

    def info(self, json_output=False):
        shadow_file_path = '/etc/shadow'
        user_info = self.parse_shadow_file(shadow_file_path)
        info_descriptions = {
            1: "deleted password",
            2: "blocked password",
            4: "temporary password",
            8: "blocked account",
            16: "invalid expire date"
        }

        result = {}

        for user, info in user_info.items():
            flags = []
            for flag_value, description in sorted(info_descriptions.items(), reverse=True):
                if info >= flag_value:
                    flags.append(description)
                    info -= flag_value
            result[user] = flags

        if json_output:
            return json.dumps(result, indent=4)
        else:
            return result

    def status(self, directory: str = None, json_output=False):
        user_info = self.parse_shadow_file()
        total_users = len(user_info)
        blocked_passwords = sum(1 for flags in user_info.values() if flags & self.uaBlockedPassword)
        deleted_passwords = sum(1 for flags in user_info.values() if flags & self.uaDeletedPassword)

        status_info = {
            "total_users": total_users,
            "blocked_passwords": blocked_passwords,
            "deleted_passwords": deleted_passwords,
        }

        if json_output:
            return json.dumps(status_info, indent=4)
        else:
            return status_info

    def id(self) -> str:
        return self.plugin_id

    def state(self) -> str:
        return self.state_value
