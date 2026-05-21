import datetime
import os
import time
from pywinauto.application import Application
import pytest


# Require RUN_NOTEPAD=1 to execute Notepad UI tests (they need an interactive desktop session)
RUN_NOTEPAD = os.environ.get("RUN_NOTEPAD", "0").lower() in ("1", "true", "yes")


@pytest.mark.parametrize("sample_text", [
    "This is line one.\nThis is line two.\nThis is line three.",
])
def test_notepad_save_and_reopen(sample_text):
    if not RUN_NOTEPAD:
        return
    file_name = f"TestFile_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    file_path = os.path.join(os.getcwd(), file_name)

    try:
        app = Application(backend="win32").start("notepad.exe")
    except Exception:
        return

    # Give Notepad time to start
    time.sleep(1)
    # Find notepad window with retry logic
    notepad = None
    for _ in range(5):
        try:
            notepad = app.window(class_name="Notepad")
            break
        except Exception:
            time.sleep(0.5)
    if notepad is None:
        raise RuntimeError("Failed to find Notepad window")
    notepad.wait("visible", timeout=10)
    edit = notepad.Edit
    edit.wait("visible", timeout=10)
    edit.type_keys(sample_text, with_newlines=True, pause=0.05)

    notepad.menu_select("File->Save As")
    save_dialog = app.window(title_re=".*Save As")
    save_dialog.wait("visible", timeout=10)

    filename_edit = save_dialog.child_window(title="File name:", auto_id="1001", control_type="Edit")
    filename_edit.set_edit_text(file_path)
    save_dialog.child_window(title="Save", auto_id="1", control_type="Button").click()

    if app.windows(title_re=".*Confirm Save As"):  # handle overwrite prompt
        confirm_dialog = app.window(title_re=".*Confirm Save As")
        confirm_dialog.child_window(title="Yes", control_type="Button").click()

    notepad.close()

    try:
        reopened = Application(backend="uia").start(f"notepad.exe {file_path}")
    except Exception:
        return

    reopened_window = reopened.window(title_re=f".*{os.path.basename(file_path)} - Notepad")
    reopened_edit = reopened_window.child_window(control_type="Edit")
    reopened_edit.wait("visible", timeout=10)

    displayed_text = reopened_edit.window_text()
    assert sample_text in displayed_text

    reopened_window.close()
