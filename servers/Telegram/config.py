import hashlib
import json
import os

directory = os.path.dirname(__file__)
config_file = os.path.join(directory, "config.json")
with open(config_file, "a+", encoding="utf8") as f:
    f.seek(0)
    config = json.load(f)["config"]
token_telegram = config["token_telegram"]["value"]
hashed_telegram_token = hashlib.sha256(token_telegram.encode('utf-8')).hexdigest()
telegram_path = "/telegram" + hashed_telegram_token
print("Путь сервера Телеграм: " + telegram_path)
