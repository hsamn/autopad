import cv2
import numpy as np

from autopad.config import DETECT
from autopad.utils.logger import log_image, get_logger

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
    logger.info(f"Loading templates for \"{name}\"")
    detect[name] = {
        "templates": []
    }
    for i, template in enumerate(entity["templates"]):
        template_path = template["path"]
        mask_threshold = template["mask_threshold"]
        img, mask = get_template(template_path, mask_threshold)
        detect[name]["templates"].append({
            "img": img,
            "mask": mask
        })
        logger.info(f"Template ({i + 1}) loaded")

def calc_ccoeff(img, template_img, template_mask):
    result = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF_NORMED, mask=template_mask)
    result[np.isinf(result)] = 0
    result[np.isnan(result)] = 0

    # I think of using the following line to detect night mode in some cases
    # since in a lot of times, night mode is just the inverse of the image
    # and the ccoeff will be negatively high when matching the inverse image

    min_val, val, min_loc, loc = cv2.minMaxLoc(result)
    h, w = template_img.shape[:2]
    logger.info(f"Template size {(w, h)}")
    logger.info(f"Max CCOEFF {val} at {loc}")
    logger.info(f"Min CCOEFF {min_val} at {min_loc}")
    return loc, val

def calc_inv_sqdiff(img, loc, cache_match, cache_mask):
    (x, y), (h, w) = loc, cache_match.shape[:2]
    match = img[y:y+h, x:x+w]
    sqdiff_val = cv2.matchTemplate(match, cache_match, cv2.TM_SQDIFF_NORMED, mask=cache_mask)[0, 0]
    sqdiff_inv_val = 1 - sqdiff_val
    logger.info(f"Inv-SQDIFF {sqdiff_inv_val} at {(x, y)} with size {(w, h)}")
    return loc, (w, h), sqdiff_inv_val

detected_cache = dict()
def scan_templates(img, entity):
    detected = dict()

    logger.info(f"Looking for {entity}")

    if entity in detected_cache:
        logger.info(f"Found cache")
        cache = detected_cache[entity]
        loc, size, val = calc_inv_sqdiff(img, cache["loc"], cache["match"], cache["mask"])
        if val > 0.75:
            logger.info(f"Cache succeeded (> 0.75)")
            detected[entity] = {
                "loc": loc,
                "size": size,
                "cached": True
            }
            return detected

    templates = detect[entity]["templates"]
    for i, template in enumerate(templates):
        logger.info(f"Trying template ({i + 1})")
        loc, val = calc_ccoeff(img, template["img"], template["mask"])
        if val <= 0.75:
            continue
        logger.info("Template succeeded (> 0.75)")
        if entity in detected:
            prev = detected[entity]
            prev_val, prev_rank = prev["val"], prev["rank"]
            if val < prev_val or (val == prev_val and i > prev_rank):
                continue
        logger.info("Best template so far")

        detected[entity] = {
            "rank": i,
            "template": template,
            "loc": loc,
            "val": val
        }

    if entity in detected:
        found = detected[entity]
        loc, template = found["loc"], found["template"]
        (x, y) = loc
        (h, w) = template["img"].shape[:2]
        template_mask = template["mask"]

        detected_cache[entity] = {
            "loc": loc,
            "match": img[y:y+h, x:x+w],
            "mask": template_mask
        }

        logger.info("Got a new cache")

        detected[entity] = {
            "loc": loc,
            "size": (w, h),
            "cached": False
        }
    return detected

img_counter = 0
def find_entities(img, entities):
    global img_counter
    img_counter += 1

    log_image(f"img_{img_counter:03d}.png", img)

    detected = dict()
    for entity in entities:
        detected.update(scan_templates(img, entity))

    for entity, found in detected.items():
        (x, y), (w, h) = found["loc"], found["size"]
        res = img.copy()

        cv2.rectangle(
            res,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        log_image(f"img_{img_counter:03d}_res_{entity}.png", res)
    return detected

