import hashlib
import json
import os

directory = os.path.dirname(__file__)
config_file = os.path.join(directory, "config.json")
with open(config_file, "a+", encoding="utf8") as f:
    f.seek(0)
    config = json.load(f)["config"]
confirmation_string = config["confirmation_string"]["value"]
token_vk = config["token_vk"]["value"]
hashed_vk_token = hashlib.sha256(token_vk.encode('utf-8')).hexdigest()
vk_path = "/vk" + hashed_vk_token
print("Путь сервера ВК: " + vk_path)
