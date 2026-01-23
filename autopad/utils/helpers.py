import json
import numpy as np
from mss.windows import MSS as mss

def read_json(file_path):
    with open(file_path, "rt", encoding="utf-8") as file:
        return json.load(file)

def ensure_unique_path(file_name, file_ext, parent_dir):
    full_name = f"{file_name}.{file_ext}"
    candidate_path = parent_dir / full_name

    counter = 2
    while candidate_path.exists():
        full_name = f"{file_name}_{counter}.{file_ext}"
        candidate_path = parent_dir / full_name
        counter += 1
    return str(candidate_path)

def get_pretty_json(json_data):
    return json.dumps(json_data, ensure_ascii = False, indent = 4)

sct = mss.mss()
monitor = sct.monitors[1]

def get_frame():
    return np.array(sct.grab(monitor))[:, :, :3]

def close_mss():
    sct.close()

