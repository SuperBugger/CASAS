import pwd
import json


class Plugin:
    SZI_NAME = "users_policy"

    def get_users_info(self):
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

    def status(self):
        users_info = self.get_users_info()
        status_info = {}
        for user in users_info:
            status_info[user['username']] = {
                'uid': user['uid'],
                'gid': user['gid']
            }
        return self._format_output(status_info)

    def info(self):
        users_info = self.get_users_info()
        info_info = {}
        for user in users_info:
            info_info[user['username']] = {
                'home_directory': user['home_directory'],
                'shell': user['shell']
            }
        return self._format_output(info_info)

    def _format_output(self, data, json_output=False):
        if json_output:
            return json.dumps(data, indent=4)
        else:
            formatted_output = ''
            for username, info in data.items():
                formatted_output += f"User: {username}\n"
                for key, value in info.items():
                    formatted_output += f"{key.capitalize()}: {value}\n"
                formatted_output += '\n'
            return formatted_output
