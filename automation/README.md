# Automation Assignment

This folder contains Python automation scripts for the provided assignment scenarios.

## Folder Structure

- `automation/requirements.txt` - Python dependency list
- `automation/web_test.py` - Web application automation for Automation Exercise
- `automation/notepad_test.py` - Windows Notepad automation using pywinauto
- `automation/mobile_test.py` - Mobile Calculator automation using Appium
- `automation/api_test.py` - API automation for Reqres.in
- `automation/run_all.py` - Consolidated runner for all scenarios
- `automation/utils.py` - Shared helper functions

## Setup

1. Open a terminal in the workspace root: `c:\Users\prana\VSCode Projects`
2. Install dependencies:

   ```powershell
   "C:/Program Files/Python314/python.exe" -m pip install -r automation/requirements.txt
   ```

3. Optional: create a Python virtual environment and install dependencies there.

## Execution

### Run all tests with pytest

```powershell
"C:/Program Files/Python314/python.exe" -m pytest automation --html=automation/report.html
```

### Run all tests with the consolidated runner

```powershell
"C:/Program Files/Python314/python.exe" automation/run_all.py
```

### Run a single scenario

- Web: `python -m pytest automation/web_test.py -q`
- Notepad: `python -m pytest automation/notepad_test.py -q`
- Mobile: `python -m pytest automation/mobile_test.py -q`
- API: `python -m pytest automation/api_test.py -q`

## Notes

- `automation/mobile_test.py` expects Appium server available at `http://127.0.0.1:4723/wd/hub`.
- `automation/api_test.py` reads `REQRES_API_KEY` from the environment because `reqres.in` now requires an API key for POST/PUT/DELETE operations.
- The Notepad script uses `pywinauto` and will only run on Windows.

## Reporting

Use `pytest --html=report.html` to generate an HTML execution report. The generated report will be written to the working directory.
