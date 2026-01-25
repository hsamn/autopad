import requests
import time
from autopad.config import API_URL, ALT_JSON_PATH, NEW_LINE
from autopad.utils.helpers import read_json, get_pretty_json
from autopad.utils.logger import get_logger

logger = get_logger(__name__)

def fetch_api_json():
    logger.info("Retrieving posts from json api")
    for i in range(3):
        logger.info(f"Attempt ({i + 1})")
        try:
            time.sleep(1)
            response = requests.get(
                API_URL,
                headers={"Accept": "application/json"},
                timeout=10
            )

            response.raise_for_status()
            logger.info("Got posts from json api")
            return response.json()
        except Exception as e:
            logger.warning(f"Could not retrieve posts from json api endpoint: {e}")
    logger.warning("Failed: Falling back to alt posts")
    return read_json(ALT_JSON_PATH)

POSTS = fetch_api_json()
for i, post in enumerate(POSTS):
    logger.info(f"Reformatting post ({i + 1})")
    logger.info(f"old post: {NEW_LINE}{get_pretty_json(post)}")
    new_post = {
        "content": f"Title: {post['title']}{NEW_LINE}{NEW_LINE}{post['body']}",
        "name": f"post_{post['id']}",
        "ext": "txt"
    }
    logger.info(f"new post: {NEW_LINE}{get_pretty_json(new_post)}")
    POSTS[i] = new_post

