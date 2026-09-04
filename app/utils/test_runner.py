import os
import subprocess
import sys
from pathlib import Path


TEST_TIMEOUT_SECONDS = int(os.getenv("GENERATED_TEST_TIMEOUT", "120"))


def run_project_tests(project_path: str) -> dict:
    """Run pytest inside the generated project and return its real output."""
    project_directory = Path(project_path).resolve()

    if not project_directory.is_dir():
        return {
            "status": "FAIL",
            "return_code": None,
            "output": f"Project directory does not exist: {project_directory}",
        }

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--tb=long"],
            cwd=project_directory,
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") + (exc.stderr or "")
        return {
            "status": "FAIL",
            "return_code": None,
            "output": f"pytest timed out after {TEST_TIMEOUT_SECONDS} seconds.\n{output}",
        }
    except OSError as exc:
        return {
            "status": "FAIL",
            "return_code": None,
            "output": f"Unable to execute pytest: {exc}",
        }

    output = (result.stdout or "") + (result.stderr or "")
    status = "PASS" if result.returncode == 0 else "FAIL"
    if result.returncode == 5:
        status = "NO_TESTS"

    return {
        "status": status,
        "return_code": result.returncode,
        "output": output.strip(),
    }
