PASSWORD_POLICY_FILE = '/etc/pam.d/common-password'


def show_difference():
    try:
        with open(PASSWORD_POLICY_FILE, 'r') as f:
            policy = f.read().splitlines()

        current_user_policy = get_current_user_password_policy()

        differences = compare_policies(policy, current_user_policy)
        print("Differences between policy and current user settings:")
        for diff in differences:
            print(diff)
    except FileNotFoundError:
        print("File {PASSWORD_POLICY_FILE} not found.")


def get_current_user_password_policy():
    # todo: получение значений парольной политики пользователя
    return 0


import crypt
import getpass
import os
import pwd
import spwd
import re

def get_encrypted_password(username):
    # Получение зашифрованного пароля из /etc/shadow
    shadow_entry = spwd.getspnam(username)
    return shadow_entry.sp_pwdp

def verify_password(username, password):
    # Получение зашифрованного пароля
    encrypted_password = get_encrypted_password(username)

    # Проверка введенного пароля
    return crypt.crypt(password, encrypted_password) == encrypted_password

def check_password_strength(password):
    if len(password) < 8:
        return False, "Password is too short. Must be at least 8 characters."

    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit."

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."

    return True, "Password meets all requirements."

def main():
    username = getpass.getuser()
    current_password = getpass.getpass("Enter current password: ")

    # Проверка правильности текущего пароля
    if not verify_password(username, current_password):
        print("Incorrect current password.")
        return

    # Проверка соответствия пароля нормам СЗИ
    strength_ok, message = check_password_strength(current_password)
    if strength_ok:
        print("Current password meets the security requirements.")
    else:
        print(f"Current password does not meet the security requirements: {message}")

if name == "main":
    main()





def compare_policies(policy, current_user_policy):
    return [line for line in policy if line not in current_user_policy]