import json
import os
import os.path

CONFIG_DIR = os.path.expanduser(os.path.join('~', '.config', 'anon.ai'))
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

def read():
    if not os.path.isfile(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE) as f:
        return json.load(f)

def write(data):
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    with open(CONFIG_FILE, 'w') as f:
        f.write(json.dumps(data))
