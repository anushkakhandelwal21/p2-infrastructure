
from unittest.mock import patch

from auto_fixer import apply_and_verify_fix


def test_rejects_invalid_ai_response():
    with patch(
        "auto_fixer.analyze_issue",
        return_value={
            "success": True,
            "parsed_analysis": {
                "proposed_fix": {
                    "code": "this is not valid python !!!"
                }
            }
        },
    ):
        result = apply_and_verify_fix(
            issue={"number": 1, "title": "Test"},
            test_output="failed",
        )

    assert result["success"] is False
    assert "syntax" in result["message"].lower()


def test_rejects_unexpected_function():
    with patch(
        "auto_fixer.analyze_issue",
        return_value={
            "success": True,
            "parsed_analysis": {
                "proposed_fix": {
                    "code": "def delete_everything():\n    pass\n"
                }
            }
        },
    ):
        result = apply_and_verify_fix(
            issue={"number": 1, "title": "Test"},
            test_output="failed",
        )

    assert result["success"] is False
    assert "calculate_average" in result["message"]
