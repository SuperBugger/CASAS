PASSWORD_POLICY_FILE = '/etc/pam.d/common-password'


def show_status():
    try:
        with open(PASSWORD_POLICY_FILE, 'r') as f:
            policy = f.read()
            print("Password Policy:")
            print(policy)
    except FileNotFoundError:
        print("File {PASSWORD_POLICY_FILE} not found.")
