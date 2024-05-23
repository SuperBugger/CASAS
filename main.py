#!/usr/bin/env python3
import subprocess
import sys

from core import PluginManager
import threading


def run_cli():
    subprocess.run([sys.executable, 'cli.py', '--run_plugins'])


# def run_web():
#     subprocess.run(web)

if __name__ == "__main__":
    cli_thread = threading.Thread(target=run_cli)
    # web_thread = threading.Thread(target=run_web)

    cli_thread.start()
    # web_thread.start()

    cli_thread.join()
    # web_thread.join()

    # manager = PluginManager()
    # manager.load_plugins()
    # manager.run_plugins()
