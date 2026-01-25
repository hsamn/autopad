import logging
import cv2

from autopad.config import LOG_LEVEL, LOGS_TXT_FILE, LOGS_IMGS_DIR

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        handler = logging.FileHandler(LOGS_TXT_FILE, encoding = "utf-8")
        formatter = logging.Formatter("%(asctime)s | [%(levelname)s] | %(name)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = get_logger(__name__)

def log_image(img_name, img):
    logger.info(f"Logging image to: \"{img_name}\"")
    cv2.imwrite(str(LOGS_IMGS_DIR / img_name), img)

