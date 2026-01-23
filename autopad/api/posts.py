import requests
from autopad.config import API_URL, ALT_JSON_PATH, NEW_LINE
from autopad.utils.helpers import read_json, get_pretty_json
from autopad.utils.logger import get_logger

logger = get_logger(__name__)

def fetch_api_json():
    for count in range(1, 4):
        try:
            logger.info(f"Retrieving posts attempt: {count}")
            response = requests.get(
                API_URL,
                headers={"Accept": "application/json"},
                timeout=10
            )

            response.raise_for_status()
            logger.info("Got the json from the API")
            return response.json()
        except Exception as e:
            logger.warn(f"Couldn't retrieve posts: {e}")
    logger.warn("Falling back to alternative posts")
    return read_json(ALT_JSON_PATH)

POSTS = fetch_api_json()

for i, post in enumerate(POSTS):
    title, body, post_id = post["title"], post["body"], post["id"]
    new_post = {
        "content": f"Title: {title}{NEW_LINE}{NEW_LINE}{body}",
        "name": f"post_{post_id}",
        "ext": "txt"
    }
    POSTS[i] = new_post
    logger.info(f"Reformatted {i + 1}: {NEW_LINE}{get_pretty_json(new_post)}")

