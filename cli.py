import argparse
from core import PluginManager


def main():
    parser = argparse.ArgumentParser(description="CASAS cli tool")
    parser.add_argument('--run-plugins', action='store_true', help='Run all plugins')
    args = parser.parse_args()

    if args.run_plugins:
        manager = PluginManager()
        manager.load_plugins()
        results = manager.run_plugins()
        for name, result in results.items():
            print(f"{name}: {result}")


if __name__ == 'main':
    main()
