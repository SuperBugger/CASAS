import subprocess
from typing import Dict


def run_command(command: list) -> Dict[str, str]:
    result = {"stdout": "", "stderr": ""}
    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        result["stdout"] = process.stdout.strip()
        result["stderr"] = process.stderr.strip()
    except FileNotFoundError:
        result["stderr"] = f"{command[0]} utility not found."
    except subprocess.CalledProcessError as e:
        result["stdout"] = process.stdout.strip()
        result["stderr"] = f"Error occurred while running {' '.join(command)}: {str(e)}"
    return result