from . import password_policy_status
from . import password_policy_diff


def show_status():
    password_policy_status.show_status()


def show_difference():
    password_policy_diff.show_difference()