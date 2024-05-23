#!/usr/bin/env python3

import sys
from cli import parse_arguments
from app import core


def main():
    args = parse_arguments(sys.argv[1:])
    core.run(args)


if __name__ == "__main__":
    main()
