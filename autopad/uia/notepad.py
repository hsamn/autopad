import time
import pyautogui
from pywinauto import Desktop, Application

from autopad.vision.find import find_entities
from autopad.utils.helpers import get_frame, ensure_unique_path
from autopad.utils.logger import get_logger
from autopad.config import OUT_PATH

logger = get_logger(__name__)

entities = ["notepad"]
desktop = Desktop(backend="uia")
application = Application(backend="uia")

def get_notepad_center():
    for _ in range(6):
        logger.info("Pressing Win + m to show desktop")
        pyautogui.hotkey('win', 'm')
        time.sleep(3)
        res = find_entities(get_frame(), entities)
        if "notepad" in res and res["notepad"]["cached"]:
            return res["notepad"]["center"]
        logger.info("Notepad not found or found but not cached")
    raise TimeoutError("Finding notepad icon timeout")

def get_notepads_pid_hwnd():
    return {(w.process_id(), w.handle) for w in desktop.windows(title_re=".*Untitled.*Notepad.*", top_level_only=True, control_type="Window")}

def open_notepad():
    x, y = get_notepad_center()
    logger.info(f"Moving the cursor to the icon position ({x}, {y})")
    pyautogui.moveTo(x, y, duration=0.2)
    logger.info("Double clicking the icon")
    past_set = get_notepads_pid_hwnd()
    pyautogui.doubleClick(interval=0.1)
    logger.info("Waiting for notepad to open")
    for _ in range(20):
        time.sleep(1)
        current_set = get_notepads_pid_hwnd()
        new_set = current_set - past_set
        if new_set:
            logger.info(f"Got some new Notepads (pid, hwnd): {new_set}")
            pid, hwnd = new_pids.pop()
            logger.info(f"Picked: {(pid, hwnd)}")
            app = application.connect(process=pid)
            window = app.window(handle=hwnd)
            return app, window
        logger.info("Notepad isn't opened yet")
    raise TimeoutError("No new notepad window appeared, waiting for notepad timeout")

def paste_and_save(window, text, file_name, file_ext):
    logger.info("Saving clipboard info")
    original_clipboard = pyperclip.paste()
    DONE = False

    try:
        app, window = open_notepad()

        logger.info("Waiting window to be visible")
        window.wait("visible", timeout=10)
        logger.info("Setting focus to it")
        window.set_focus()

        logger.info("Copying text")
        pyperclip.copy(text)
        logger.info("Pasting text")
        window.type_keys("^v")
        time.sleep(0.5)

        logger.info("Opening Save As dialog")
        window.type_keys("^+s")

        save_as = window.child_window(title_re=".*Save [Aa]s.*", top_level_only=True, control_type="Window")
        logger.info("Waiting for the save as dialog to be visible")
        save_as.wait("visible", timeout=10)

        logger.info("Ensuring the saving path is unique")
        save_to = ensure_unique_path(file_name, file_ext, OUT_PATH)

        logger.info("Copying path")
        pyperclip.copy(save_to)
        logger.info("Pasting path")
        save_as.set_focus()
        save_as.type_keys("^v")
        time.sleep(0.5)

        logger.info("Pressing Enter")
        save_as.type_keys("{ENTER}")

        logger.info("Waiting until the save as window disappear")
        save_as.wait_not("visible", timeout=10)

        logger.info("Closing")
        window.close()
        logger.info("Waiting until the main window disappear")
        window.wait_not("visible", timeout=5)
        DONE = True

    except Exception as e:
        logger.warn(f"Could not automate the paste and save process: ERROR: {e}")
        DONE = False

    finally:
        logger.info("Restoring the original clipboard")
        pyperclip.copy(original_clipboard)

    return DONE

