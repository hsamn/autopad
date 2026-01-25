import logging
from pathlib import Path

print("Initiating configuration and logger")

# path to the assets
ASSETS_PATH = Path("autopad") / "assets"

# alternative data to be fetched instead of failing
ALT_JSON_PATH = str(ASSETS_PATH / "posts" / "alt.json")

# paths to detect notepad
NOTEPAD_ICONS_PATH = ASSETS_PATH / "detect" / "notepad"

# path to save files
OUT_PATH = Path.home() / "Desktop" / "tjm-project"
print(f"Making sure \"{str(OUT_PATH)}\" exists")
OUT_PATH.mkdir(parents = True, exist_ok = True)

# logs dir path
LOGS_DIR = Path("logs")
print(f"Making sure \"{str(LOGS_DIR)}\" exists")
LOGS_DIR.mkdir(parents = True, exist_ok = True)

# log level
LOG_LEVEL = logging.INFO

# logs text file path
LOGS_TXT_FILE = LOGS_DIR / "log.txt"
print(f"Making sure \"{str(LOGS_TXT_FILE)}\" is empty")
if LOGS_TXT_FILE.exists():
    LOGS_TXT_FILE.unlink()
LOGS_TXT_FILE = str(LOGS_TXT_FILE)

# logs images dir path
LOGS_IMGS_DIR = LOGS_DIR / "imgs"
print(f"Making sure \"{str(LOGS_IMGS_DIR)}\" exists")
LOGS_IMGS_DIR.mkdir(parents = True, exist_ok = True)

# monitor number: 1, 2, 3, ...
MON_ID = 1

# new line char to fit windows
NEW_LINE = "\r\n"

# the endpoint url
API_URL = "https://jsonplaceholder.typicode.com/posts"

# things to detect
DETECT = {
    "notepad": {
        "templates": [
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_new_link_96x96.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_new_link_48x48.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_new_link_32x32.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_96x96.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_48x48.png"),
                "mask_threshold": 1
            },
            {
                "path": str(NOTEPAD_ICONS_PATH / "new_icon_32x32.png"),
                "mask_threshold": 1
            }
        ]
    }
}

