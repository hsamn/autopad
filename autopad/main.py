import time
import pyperclip
from mss.windows import MSS as mss

from autopad.config import MON_ID
from autopad.api.posts import POSTS
from autopad.utils.logger import get_logger
from autopad.uia.notepad import get_notepad_center, open_notepad, paste_and_save

logger = get_logger(__name__)

def handle_post(content, name, ext, sct, monitor):
    for i in range(3):
        time.sleep(1)
        logger.info(f"Attempt ({i + 1})")
        try:
            logger.info("Looking for notepad center")
            x, y = get_notepad_center(sct, monitor)
            logger.info(f"Got notepad center {(x, y)}")
            logger.info("Opening notepad")
            app, window = open_notepad(x, y)
            logger.info("Saving the user's clipboard")
            original_clipboard = pyperclip.paste()
            logger.info("Pasting and saving")
            try:
                paste_and_save(window, content, name, ext)
                logger.info("Closing the window")
                window.close()
                logger.info("Waiting for it to not be existing")
                window.wait_not("exists")
            finally:
                logger.info("Restoring user's clipboard")
                pyperclip.copy(original_clipboard)
            logger.info("Post task succeeded")
            return
        except Exception as e:
            logger.warning(f"Failed to complete the task on the post: {e}")
    raise TimeoutError("Could not perform task after trying 3 times with 1 second delay")

def main():
    with mss() as sct:
        logger.info("Initiated mss session")
        monitor = sct.monitors[MON_ID]
        logger.info("Got monitor info")
        logger.info("Proceeding with the task on posts")
        for i, post in enumerate(POSTS):
            logger.info(f"Trying post ({i + 1})")
            try:
                handle_post(post["content"], post["name"], post["ext"], sct, monitor)
                logger.info("Post succeeded")
            except Exception as e:
                logger.warning(f"Post failed after 3 attempts. Closing. {e}")
                break

if __name__ == "__main__":
    main()

