import argparse
import subprocess


def run_cli(args):
    subprocess.run(['python3', 'cli_runner.py'] + args)


def run_web_server():
    from web_server import app
    app.run(debug=True)


def main():
    parser = argparse.ArgumentParser(description="CASAS System")
    parser.add_argument('--mode', choices=['cli', 'web'], required=True,
                        help="Mode to run: 'cli' for command line interface, 'web' for web server")
    args, unknown = parser.parse_known_args()

    if args.mode == 'cli':
        run_cli(unknown)
    elif args.mode == 'web':
        run_web_server()


if __name__ == '__main__':
    main()
