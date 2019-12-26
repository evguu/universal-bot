import requests
from servers.Telegram import config as telegram_config

URL = "https://api.telegram.org/bot{}/".format(telegram_config.token_telegram)


def set_webhook(url):
    r = requests.post(URL + "setWebhook?url=" + url + telegram_config.telegram_path)
    return r.json()


def delete_webhook():
    r = requests.get(URL + "deleteWebhook")
    return r.json()


def get_username(user_id):
    url = URL + "getChat?chat_id=" + str(user_id)
    r = requests.get(url).json()
    if r["ok"]:
        return r["result"]["username"]
    return False


def main():
    if input("Учтите, что прошлая привязка сотрется. Для подтверждения введите ПОНЯЛ.") != "ПОНЯЛ":
        print("Операция отменена.")
        return
    delete_webhook()
    resp = set_webhook(input("Куда биндить будем? "))
    if resp["ok"]:
        print("Успешно привязано.")
    else:
        print("Привязка не удалась. Ответ сервера: {}".format(resp["description"]))


if __name__ == '__main__':
    main()
