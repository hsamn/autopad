import cv2
import numpy as np

from autopad.config import DETECT
from autopad.utils.logger import get_logger, log_image

logger = get_logger(__name__)

### TODO ###

# add to each template a weight (from 0 to 1) instead of ranks
# find a way to estimate the final score using the following:
# - the weights
# - ccoeff score
# - the number of matches passing 50% or 75% (±50% for ccoeff is great)
# - grouping similar matches together (each icon has a clickable area)
# also, try to make use of the negative ccoeff number, it seems interesting..
# instead of trying out all the icon sizes (brute-force style) try to detect the desktop icon sizes being used using e.g. edge detection
# use a better caching approach

def get_template(file_path, mask_threshold):
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    img, mask = img[:, :, :3], img[:, :, 3]
    mask[mask >= mask_threshold] = 255
    mask[mask < mask_threshold] = 0
    return img, mask

detect = dict()
for name, entity in DETECT.items():
    detect[name] = {
        "templates": []
    }
    for i, info in enumerate(entity["templates"]):
        template_path = info["path"]
        mask_threshold = info["mask_threshold"]

        logger.info(f"Loading template {i + 1} for entity {name} from {template_path}")

        img, mask = get_template(template_path, mask_threshold)
        detect[name]["templates"].append({
            "img": img,
            "mask": mask
        })

        log_image("template_img", "template_img", img)
        log_image("template_img", "template_mask", mask)

def calc_ccoeff(img, template_img, mask):
    result = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF_NORMED, mask=mask)
    result[np.isinf(result)] = 0
    result[np.isnan(result)] = 0
    # I think of using the following line to detect night mode in some cases
    # since in a lot of times, night mode is just the inverse of the image
    # and the ccoeff will be negatively high when matching the inverse image
    n_val, val, n_loc, loc = cv2.minMaxLoc(result)
    logger.info(f"Negative ccoeff is {n_val} at {n_loc}")
    return loc, val

def calc_sqdiff(img, template_img):
    return cv2.matchTemplate(img, template_img, cv2.TM_SQDIFF_NORMED)[0, 0]

detected_cache = dict()
def scan_templates(img, templates, entity):
    entities = dict()

    if entity in detected_cache:
        logger.info(f"Found cache in {entity}")
        (x, y), cache_match = detected_cache[entity]["loc"], detected_cache[entity]["match"]
        h, w = cache_match.shape[:2]
        match = img[y:y+h, x:x+w]
        cache_val = calc_sqdiff(match, cache_match)
        logger.info(f"Cache sqdiff-inv score: {1 - cache_val}")
        if cache_val < 0.25:
            logger.info("Cache Succeeded > 0.75")
            center = detected_cache[entity]["center"]
            entities[entity] = {
                "center": center,
                "cached": True
            }
            return entities
        logger.info("Cache Faild <= 0.75")

    for i, template in enumerate(templates):
        logger.info(f"Trying template {i + 1}")
        loc, val = calc_ccoeff(img, template["img"], template["mask"])
        logger.info(f"Templiate ccoeff scored: {val} at top-left: {loc}")
        if val > 0.75:
            logger.info(f"Templiate Succeeded > 0.75")
            if entity not in entities or (val > entities[entity]["val"] or (val == entities[entity]["val"] and i < entities[entity]["rank"])):
                logger.info(f"Best Template So Far")
                entities[entity] = {
                    "rank": i,
                    "template": template,
                    "loc": loc,
                    "val": val
                }

    if entity in entities:
        (x, y), (h, w) = entities[entity]["loc"], entities[entity]["template"]["img"].shape[:2]
        center = (x + (w - 1) / 2, y + (h - 1) / 2)
        entities[entity] = {
            "center": center,
            "cached": False
        }
        detected_cache[entity] = {
            "loc": (x, y),
            "center": center,
            "match": img[y:y+h, x:x+w]
        }
    return entities

def find_entities(img, entities):
    log_image("img", "img", img)
    detected = dict()
    for entity in entities:
        logger.info(f"Looking for {entity}")
        detected.update(scan_templates(img, detect[entity]["templates"], entity))
    for entity, res in detected.items():
        cached = res["cached"]
        cache = detected_cache[entity]
        (x, y), center, cache_img = cache["loc"], cache["center"], cache["match"]
        (h, w) = cache_img.shape[:2]
        logger.info(f"Detected: {entity}")
        log_image("img", "res", img[y:y+h, x:x+w])
        if not cached:
            log_image("img", "cache", cache_img)
    return detected

