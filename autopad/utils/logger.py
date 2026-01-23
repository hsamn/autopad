import logging
import cv2
from pathlib import Path

LOG_LEVEL = logging.INFO
LOG_IMGS = True

LOG_PATH = Path("logs")
LOG_IMGS_DIR = LOG_PATH / "imgs"
LOG_FILE_PATH = str(LOG_PATH / "log.txt")

LOG_IMGS_DIR.mkdir(parents = True, exist_ok = True)
LOG_PATH.mkdir(parents = True, exist_ok = True)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE_PATH)
        formatter = logging.Formatter("%(asctime)s | [%(levelname)s] | %(name)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = get_logger(__name__)

img_logs = dict()
img_names_logs = dict()
def log_image(img_cat, img_name, img):
    if img_cat == img_name:
        if img_cat in img_logs:
            img_logs[img_cat] += 1
        else:
            img_logs[img_cat] = 1
    if img_name in img_names_logs:
        img_names_logs[img_name] += 1
    else:
        img_names_logs[img_name] = 1
    logger.info(f"Got a new {img_cat}:{img_logs[img_cat]}, {img_name}:{img_names_logs[img_name]}")
    if LOG_IMGS:
        file_name = f"{img_cat}_{img_name}_{img_logs[img_cat]:03d}_{img_names_logs[img_name]:03d}.png"
        cv2.imwrite(str(LOG_IMGS_DIR / file_name), img)

