from . import password_policy

ASPECTS = {
    'password_policy': password_policy
}


def list_aspects():
    for aspect in ASPECTS:
        print(aspect)


def show_status(aspect):
    if aspect in ASPECTS:
        ASPECTS[aspect].show_status()
    else:
        print("Aspect '{aspect}' is not implemented.")


def show_difference(aspect):
    if aspect in ASPECTS:
        ASPECTS[aspect].show_difference()
    else:
        print("Aspect '{aspect}' is not implemented.")


def run(args):
    if args.command == 'list':
        list_aspects()
    elif args.command == 'status':
        show_status(args.aspect)
    elif args.command == 'difference':
        show_difference(args.aspect)
    else:
        print("Unknown command. Use --help for more information.")
