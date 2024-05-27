class Plugin:
    SZI_NAME = "password_policy"

    def get_password_policy(self):
        try:
            with open('/etc/passwd', 'r') as passwd_file:
                return passwd_file.read()
        except FileNotFoundError:
            return "/etc/passwd file not found."

    def status(self):
        password_policy_info = self.get_password_policy()
        return f"Password policy status: {password_policy_info}"

    def info(self):
        password_policy_info = self.get_password_policy()
        return self._format_output(password_policy_info)

    def _format_output(self, data):
        return data