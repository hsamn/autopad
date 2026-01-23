from pathlib import Path
from autopad.utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Init configurations")

# path to the assets
ASSETS_PATH = Path("autopad") / "assets"

# alternative data to be fetched instead of failing
ALT_JSON_PATH = str(ASSETS_PATH / "posts" / "alt.json")

# paths to detect notepad
NOTEPAD_ICONS_PATH = ASSETS_PATH / "detect" / "notepad"

# path to save files
OUT_PATH = Path.home() / "Desktop" / "tjm-project"

# new line char to fit windows
NEW_LINE = "\r\n"

# the endpoint url
API_URL = "https://jsonplaceholder.typicode.com/posts"

# things to detect
DETECT = {
    "notepad": {
        "templates": [
            {
                "path": str(NOTEPAD_ICONS_PATH / "old_icon_new_link_48x48.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "old_icon_new_link_24x24.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_new_link_64x64.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_new_link_48x48.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_new_link_40x40.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_new_link_32x32.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "old_icon_48x48.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "old_icon_24x24.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_64x64.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_48x48.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_40x40.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_32x32.png"),
                "mask_threshold": 1
            }
        ]
    }
}

# make sure it exists
logger.info(f"Making sure {str(OUT_PATH)} exists")
OUT_PATH.mkdir(parents = True, exist_ok = True)

