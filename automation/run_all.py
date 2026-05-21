import os
import sys
from pathlib import Path

import pytest

# Environment variables used by this runner:
# - RUN_WEB=1       : include automation/web_test.py
# - RUN_NOTEPAD=1   : include automation/notepad_test.py
# - RUN_MOBILE=1    : include automation/mobile_test.py
# - REQRES_RUN_WRITE=1 : enable Reqres API write tests in automation/api_test.py
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

automation_dir = Path(__file__).resolve().parent


def main():
    report_path = automation_dir / "report.html"

    if os.environ.get("REQRES_RUN_WRITE", "0").lower() not in ("1", "true", "yes"):
        print("WARNING: REQRES_RUN_WRITE is not enabled. API write tests will be skipped unless REQRES_RUN_WRITE=1 is set.")

    test_files = [automation_dir / "smoke_test.py", automation_dir / "api_test.py"]

    if os.environ.get("RUN_WEB", "0").lower() in ("1", "true", "yes"):
        test_files.append(automation_dir / "web_test.py")
    if os.environ.get("RUN_NOTEPAD", "0").lower() in ("1", "true", "yes"):
        test_files.append(automation_dir / "notepad_test.py")
    if os.environ.get("RUN_MOBILE", "0").lower() in ("1", "true", "yes"):
        test_files.append(automation_dir / "mobile_test.py")

    return_code = pytest.main([
        *map(str, test_files),
        "--html=" + str(report_path),
        "--self-contained-html",
    ])
    sys.exit(return_code)


if __name__ == "__main__":
    main()
