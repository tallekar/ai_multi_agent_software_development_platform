import ast
from pathlib import PurePath


def validate_generated_files(files: dict[str, str]) -> dict:
    """
    Perform cheap local validation.
    No LLM call is required.
    """

    issues = []
    checked = 0

    for filename, content in files.items():

        suffix = PurePath(filename).suffix.lower()

        # Validate Python syntax locally
        if suffix == ".py":

            checked += 1

            try:
                ast.parse(
                    content,
                    filename=filename
                )

            except SyntaxError as exc:

                issues.append(
                    f"{filename}: "
                    f"syntax error at line {exc.lineno}: "
                    f"{exc.msg}"
                )

    if not files:
        issues.append(
            "No FILE blocks were detected."
        )

    return {
        "status": "PASS" if not issues else "FAIL",
        "files": list(files.keys()),
        "python_files_checked": checked,
        "issues": issues
    }


def compact_validation_summary(validation: dict) -> str:

    issues = validation.get("issues", [])

    if issues:
        issue_text = "\n".join(
            f"- {issue}"
            for issue in issues
        )
    else:
        issue_text = "- None"

    return (
        f"STATUS: {validation.get('status')}\n"
        f"FILES: "
        f"{', '.join(validation.get('files', [])) or 'None'}\n"
        f"PYTHON_FILES_CHECKED: "
        f"{validation.get('python_files_checked', 0)}\n"
        f"ISSUES:\n"
        f"{issue_text}"
    )