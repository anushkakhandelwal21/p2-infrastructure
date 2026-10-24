
import subprocess


def run_gh_command(args, cwd=None):
    """Run a GitHub CLI command and return its result."""
    try:
        result = subprocess.run(
            ["gh", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "return_code": result.returncode
        }

    except FileNotFoundError:
        return {
            "success": False,
            "output": "",
            "error": "GitHub CLI (gh) is not installed or not in PATH.",
            "return_code": -1
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "GitHub command timed out.",
            "return_code": -1
        }
