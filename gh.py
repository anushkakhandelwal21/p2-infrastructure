
import subprocess
from pathlib import Path


def run_gh_command(args, cwd=None, timeout=30):
    """
    Run a GitHub CLI command and return a structured result.

    Example:
        run_gh_command(["auth", "status"])
        run_gh_command(["repo", "view"])
    """
    if not isinstance(args, (list, tuple)) or not args:
        return {
            "success": False,
            "output": "",
            "error": "args must be a non-empty list or tuple.",
            "return_code": -1
        }

    if not all(isinstance(arg, str) for arg in args):
        return {
            "success": False,
            "output": "",
            "error": "All command arguments must be strings.",
            "return_code": -1
        }

    try:
        result = subprocess.run(
            ["gh", *args],
            cwd=Path(cwd).resolve() if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
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
            "error": f"GitHub command timed out after {timeout} seconds.",
            "return_code": -1
        }

    except (OSError, ValueError) as exc:
        return {
            "success": False,
            "output": "",
            "error": str(exc),
            "return_code": -1
        }

