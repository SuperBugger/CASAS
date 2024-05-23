import argparse


def parse_arguments(args):
    parser = argparse.ArgumentParser(description="CASAS cli tool")
    subparsers = parser.add_subparsers(dest='command')

    list_parser = subparsers.add_parser('list', help='List all security aspects')

    status_parser = subparsers.add_parser('status', help='Show policy values for a specific aspect')
    status_parser.add_argument('aspect', type=str, help='The name of the aspect to show')
    status_parser.add_argument('--json', action='store_true', help='Output JSON format')

    diff_parser = subparsers.add_parser('difference', help='Show differences for a specific aspect')
    diff_parser.add_argument('aspect', type=str, help='The name of the aspect to compare')

    return parser.parse_args(args)
