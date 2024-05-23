from datetime import datetime, timedelta
import json


class User:
    uaDeletedPassword = 1
    uaBlockedPassword = 2
    uaTemporaryPassword = 4
    uaBlockedAccount = 8
    uaInvalidExpireDate = 16


def analyze_user_status(user_info):
    expire_date = (datetime(1970, 1, 1) + timedelta(days=int(user_info[7]))) if user_info[7] != '' and int(
        user_info[7]) != -1 else None
    pwd_length = len(user_info[1])
    flags = 0

    if pwd_length == 0 or (pwd_length == 1 and user_info[1][0] == '!'):
        flags |= User.uaDeletedPassword

    if pwd_length > 0 and user_info[1][0] == '!':
        flags |= User.uaBlockedPassword

    if user_info[2] == '':
        flags |= User.uaTemporaryPassword

    if expire_date and expire_date < datetime.now():
        flags |= User.uaBlockedAccount

    try:
        if int(user_info[7]) == -1:
            flags |= User.uaInvalidExpireDate
    except ValueError:
        pass

    return flags


def parse_shadow_file(shadow_file_path='/etc/shadow'):
    user_status = {}
    with open(shadow_file_path, 'r') as file:
        for line in file:
            fields = line.strip().split(':')
            username = fields[0]
            user_status[username] = analyze_user_status(fields)
    return user_status


def show_status(json_output=False):
    user_status = parse_shadow_file()
    status_descriptions = {
        1: "deleted password",
        2: "blocked password",
        4: "temporary password",
        8: "blocked account",
        16: "invalid expire date"
    }

    result = {}

    for user, status in user_status.items():
        flags = []
        for flag_value, description in sorted(status_descriptions.items(), reverse=True):
            if status >= flag_value:
                flags.append(description)
                status -= flag_value
        result[user] = flags

    if json_output:
        print(json.dumps(result, indent=4))
    else:
        for user, flags in result.items():
            print(f"User: {user}, Status: {', '.join(flags)}")

