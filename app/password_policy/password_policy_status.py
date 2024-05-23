PASSWORD_POLICY_FILE = '/etc/pam.d/common-password'


def show_status():
    try:
        with open(PASSWORD_POLICY_FILE, 'r') as f:
            policy = f.read()
            retry = r'retry=(\S+)'
            minlen = r'minlen=(\S+)'
            retry = r'retry=(\S+)'
            retry = r'retry=(\S+)'
            retry = r'retry=(\S+)'


    except FileNotFoundError:
        print("File {PASSWORD_POLICY_FILE} not found.")
