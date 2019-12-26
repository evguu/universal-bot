import os
import json
directory = os.path.dirname(__file__)
config_file = os.path.join(directory, "config.json")
with open(config_file, "a+", encoding="utf8") as f:
    f.seek(0)
    config = json.load(f)["config"]
confirmation_string = config["confirmation_string"]["value"]
token_vk = config["token_vk"]["value"]
vk_path = "/vk" + token_vk
