import pwd
import json


class Plugin:
    SZI_NAME = "users_policy"

    def get_users_info(self) -> list:
        users_info = []
        for user in pwd.getpwall():
            user_info = {
                'username': user.pw_name,
                'uid': user.pw_uid,
                'gid': user.pw_gid,
                'home_directory': user.pw_dir,
                'shell': user.pw_shell
            }
            users_info.append(user_info)
        return users_info

    def get_users_status(self, json_output: bool = False) -> str:
        users_info = self.get_users_info()
        status_info = {}
        for user in users_info:
            status_info[user['username']] = {
                'uid': user['uid'],
                'gid': user['gid']
            }

        if json_output:
            return json.dumps(status_info, indent=4, ensure_ascii=False)
        else:
            formatted_output = "Users Status Information:\n"
            for username, info in status_info.items():
                formatted_output += f"User: {username}\n"
                for key, value in info.items():
                    formatted_output += f"{key.capitalize()}: {value}\n"
                formatted_output += '\n'
            return formatted_output

    def get_users_info_details(self, json_output: bool = False) -> str:
        users_info = self.get_users_info()
        info_details = {}
        for user in users_info:
            info_details[user['username']] = {
                'home_directory': user['home_directory'],
                'shell': user['shell']
            }

        if json_output:
            return json.dumps(info_details, indent=4, ensure_ascii=False)
        else:
            formatted_output = "Users Info Details:\n"
            for username, info in info_details.items():
                formatted_output += f"User: {username}\n"
                for key, value in info.items():
                    formatted_output += f"{key.capitalize()}: {value}\n"
                formatted_output += '\n'
            return formatted_output

    def status(self, json_output: bool = False) -> str:
        return self.get_users_status(json_output)

    def info(self, json_output: bool = False) -> str:
        return self.get_users_info_details(json_output)
