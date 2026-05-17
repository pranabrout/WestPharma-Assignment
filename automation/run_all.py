import os
import sys
from pathlib import Path

import pytest

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

automation_dir = Path(__file__).resolve().parent


def main():
    report_path = automation_dir / "report.html"

    if os.environ.get("REQRES_API_KEY") is None:
        print("WARNING: REQRES_API_KEY is not set. API tests requiring write operations may fail.")

    test_files = [
        automation_dir / "web_test.py",
        automation_dir / "notepad_test.py",
        automation_dir / "mobile_test.py",
        automation_dir / "api_test.py",
    ]

    return_code = pytest.main([
        *map(str, test_files),
        "--html=" + str(report_path),
        "--self-contained-html",
    ])
    sys.exit(return_code)


if __name__ == "__main__":
    main()
