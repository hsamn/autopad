import time
import pyautogui
from pywinauto import Desktop, Application
import pyperclip
import numpy as np

from autopad.vision.find import find_entities
from autopad.utils.helpers import ensure_unique_path
from autopad.utils.logger import get_logger
from autopad.config import OUT_PATH

logger = get_logger(__name__)

entities = {"notepad"}
desktop = Desktop(backend="uia")
application = Application(backend="uia")

def get_desktop(sct, monitor):
    logger.info("Pressing win + m")
    pyautogui.hotkey("win", "m")
    logger.info("Waiting...")
    time.sleep(3)
    logger.info("Taking a screenshot")
    return np.array(sct.grab(monitor))[:, :, :3]

def get_notepad_center(sct, monitor):
    logger.info("Looking for notepad")
    res = find_entities(get_desktop(sct, monitor), entities)
    if "notepad" in res:
        logger.info("Notepad found")
        res = res["notepad"]
        if res["cached"]:
            logger.info("Notepad is found cached")
            (x, y), (w, h) = res["loc"], res["size"]
            return (x + (w - 1) / 2, y + (h - 1) / 2)
        logger.info("Notepad is found but not cached")
        logger.info("Looking for it again")
        res = find_entities(get_desktop(sct, monitor), entities)
        if "notepad" in res:
            logger.info("Notepad found again")
            res = res["notepad"]
            if res["cached"]:
                logger.info("Notepad found again and cached")
                (x, y), (w, h) = res["loc"], res["size"]
                return (x + (w - 1) / 2, y + (h - 1) / 2)
            logger.info("Could not find notepad even tho it was cached")
    raise Exception("Could not find notepad icon")

def get_notepads():
    return {(w.process_id(), w.handle) for w in desktop.windows(title_re=r"(?i).*untitled.*notepad.*", visible_only=True, top_level_only=True, control_type="Window")}

def open_notepad(x, y):
    logger.info(f"Moving the mouse to {(x, y)}")
    pyautogui.moveTo(x, y, duration=0.2)
    logger.info("Getting all notepads opened now")
    past_set = get_notepads()
    logger.info("Double clicking")
    pyautogui.doubleClick(interval=0.1)
    logger.info("Waiting til new notepad")
    for _ in range(10):
        time.sleep(1)
        current_set = get_notepads()
        new_set = current_set - past_set
        if new_set:
            logger.info(f"Got a new notepads {new_set}")
            pid, hwnd = new_set.pop()
            logger.info(f"Picked {(pid, hwnd)}")
            app = application.connect(process=pid)
            window = app.window(handle=hwnd)
            return app, window
    raise TimeoutError("Timeout waiting for new notepad window to be opened")

def paste_and_save(window, text, file_name, file_ext):
    # wait for the window
    logger.info("Waiting for window to be ready")
    window.wait("ready")
    # activate and wait
    logger.info("Focusing on it")
    window.set_focus()
    logger.info("Waiting for it to be active")
    window.wait("active")
    # copy text
    logger.info("Copy text to clipboard")
    pyperclip.copy(text)
    # paste and wait a moment
    logger.info("Pasting")
    window.type_keys("^v")
    logger.info("Waiting for past")
    time.sleep(0.5)
    # save as
    logger.info("Opening save as dialog")
    window.type_keys("^+s")
    # capture save as dialog
    save_as = window.child_window(title_re=r"(?i).*save as.*", visible_only=True, top_level_only=True, control_type="Window")
    # wait for it
    logger.info("Waiting for save as dialog to be ready")
    save_as.wait("ready")
    # activate and wait
    logger.info("Focusing on it")
    save_as.set_focus()
    logger.info("Waiting for it to be active")
    save_as.wait("active")
    # ensure we have a unique path
    logger.info("Ensuring unique path")
    save_to = ensure_unique_path(file_name, file_ext, OUT_PATH)
    logger.info(f"Got \"{save_to}\"")
    # copy path
    logger.info("Copy path to clipboard")
    pyperclip.copy(save_to)
    # paste path and wait a while
    logger.info("Pasting")
    save_as.type_keys("^v")
    logger.info("Waiting for past")
    time.sleep(0.5)
    # press enter and wait for close
    logger.info("Pressing Enter")
    save_as.type_keys("{ENTER}")
    logger.info("Waiting for save as dialog to not be existing")
    save_as.wait_not("exists")

