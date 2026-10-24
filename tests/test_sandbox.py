
import sys
from sandbox import run_command


def test_python_command():
    result = run_command([
        sys.executable,
        "-c",
        "print('Sandbox test successful')"
    ])

    assert result["success"] is True
    assert "Sandbox test successful" in result["output"]


if __name__ == "__main__":
    test_python_command()
    print("Sandbox test passed!")
