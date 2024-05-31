from cli import cli as cli_command
import sys

def main():
    cli_command(prog_name='cli', args=sys.argv[1:])


if __name__ == "__main__":
    main()
