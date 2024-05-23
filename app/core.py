from . import password_policy
from .account_info import accounts_info

ASPECTS = {
    'password_policy': password_policy,
    'accounts_info': accounts_info,
}


def list_aspects():
    for aspect in ASPECTS:
        print(aspect)


def show_status(aspect, json_output=False):
    if aspect in ASPECTS:
        ASPECTS[aspect].show_status(json_output=json_output)
    else:
        print(f"Aspect '{aspect}' is not implemented.")


def show_difference(aspect):
    if aspect in ASPECTS:
        ASPECTS[aspect].show_difference()
    else:
        print(f"Aspect '{aspect}' is not implemented.")


def run(args):
    if args.command == 'list':
        list_aspects()
    elif args.command == 'status':
        show_status(args.aspect, json_output = args.json)
    elif args.command == 'difference':
        show_difference(args.aspect)
    else:
        print("Unknown command. Use --help for more information.")
