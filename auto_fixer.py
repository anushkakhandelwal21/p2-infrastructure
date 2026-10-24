
import json
import shutil
import subprocess
import sys
from pathlib import Path

from ai_engine import analyze_issue


PROJECT_DIR = Path(__file__).resolve().parent
TARGET_FILE = PROJECT_DIR / "demo_bug.py"
TEST_FILE = PROJECT_DIR / "tests" / "test_demo_bug.py"
BACKUP_FILE = PROJECT_DIR / "demo_bug.py.backup"


def apply_and_verify_fix(issue, test_output="", test_error=""):
    """Apply an AI-proposed replacement to the demo file and verify it."""

    if not TARGET_FILE.is_file() or not TEST_FILE.is_file():
        return {
            "success": False,
            "message": "Demo source file or its test file was not found."
        }

    original_code = TARGET_FILE.read_text(encoding="utf-8")

    diagnosis = analyze_issue(
        issue=issue,
        test_output=test_output,
        test_error=test_error,
        source_code=original_code
    )

    if not diagnosis.get("success"):
        return {
            "success": False,
            "message": "AI diagnosis failed.",
            "details": diagnosis.get("error", "Unknown error")
        }

    parsed = diagnosis.get("parsed_analysis")

    if not isinstance(parsed, dict):
        return {
            "success": False,
            "message": "AI did not return valid JSON. No changes applied."
        }

    proposed_fix = parsed.get("proposed_fix")

    if not isinstance(proposed_fix, dict):
        return {
            "success": False,
            "message": "AI response has no valid proposed_fix. No changes applied."
        }

    new_code = proposed_fix.get("code")

    if not isinstance(new_code, str) or not new_code.strip():
        return {
            "success": False,
            "message": "AI did not provide replacement code."
        }

    # Only allow the expected demo function in the replacement.
    if "def calculate_average(" not in new_code:
        return {
            "success": False,
            "message": "Proposed code did not contain the expected function."
        }

    if BACKUP_FILE.exists():
        return {
            "success": False,
            "message": (
                "A backup already exists. Review or rename "
                "demo_bug.py.backup before trying again."
            )
        }

    shutil.copy2(TARGET_FILE, BACKUP_FILE)

    try:
        TARGET_FILE.write_text(new_code.rstrip() + "\n", encoding="utf-8")

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(TEST_FILE),
                "-v"
            ],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
            timeout=60,
            shell=False
        )

        if result.returncode == 0:
            BACKUP_FILE.unlink()
            return {
                "success": True,
                "message": "AI-proposed fix passed the focused tests.",
                "test_output": result.stdout,
                "test_error": result.stderr,
                "ai_analysis": parsed
            }

        # Restore the original file if verification fails.
        shutil.copy2(BACKUP_FILE, TARGET_FILE)

        return {
            "success": False,
            "message": "Tests failed. Original source file restored.",
            "test_output": result.stdout,
            "test_error": result.stderr
        }

    except (OSError, subprocess.TimeoutExpired) as exc:
        shutil.copy2(BACKUP_FILE, TARGET_FILE)

        return {
            "success": False,
            "message": "Fix verification failed. Original file restored.",
            "details": type(exc).__name__
        }

    finally:
        if BACKUP_FILE.exists():
            BACKUP_FILE.unlink()
