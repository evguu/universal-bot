from apps.queue_app.app import randomize_users, save_randomized


def rerandomize():
    randomize_users()
    save_randomized()
    print("Успешно перерандомлено.")
