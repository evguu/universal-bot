import os
import json
from utils.config_edit import format_config_by_filename
directory = os.path.dirname(__file__)
config_file = os.path.join(directory, "config.json")
try:
    with open(config_file, "a+", encoding="utf8") as f:
        f.seek(0)
        config = json.load(f)["config"]
except json.decoder.JSONDecodeError:
    format_config_by_filename(config_file)
finally:
    with open(config_file, "a+", encoding="utf8") as f:
        f.seek(0)
        config = json.load(f)["config"]
    owner_id = int(config["owner_id"]["value"])
    feedback_chat_id = int(config["feedback_chat_id"]["value"])
    errors_chat_id = int(config["errors_chat_id"]["value"])
    time_offset = int(config["time_offset"]["value"])
    bot_username_in_telegram = config["bot_username_in_telegram"]["value"]
