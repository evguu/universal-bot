import json

from utils.console_menu import Menu


def get_editing_menu_for_config(config_file):
    """
    Принимает путь к файлу конфигурации и возвращает консольное меню для его редактирования.
    """

    with open(config_file, "a+") as f:
        f.seek(0)
        content = f.read()
        config = json.loads(content)["config"]

    def get_condition():
        for item in config.items():
            print(item[0] + " : " + ("В порядке" if item[1]["filled"] else "Не установлен"))

    def print_contents():
        for item in config.items():
            print("{}: {}".format(item[0], (item[1]["value"] if item[1]["filled"] else "Не установлен")))

    def get_property_editor(name):
        def property_editor():
            config[name]["value"] = input("Введите значение: ")
            if config[name]["type"] == "int":
                config[name]["value"] = int(config[name]["value"])
            config[name]["filled"] = True
            structure = {"config": config}
            with open(config_file, "w") as f:
                json.dump(structure, f, indent=4)
            print("Значение изменено.")

        return property_editor

    def reset_config():
        if input("Вы уверены, что хотите сбросить конфигурацию? Эту операцию нельзя будет отменить!\n"
                 "Для подтверждения введите ПОНЯЛ.") != "ПОНЯЛ":
            print("Операция отменена.")
            return
        for item in config.items():
            item[1]["filled"] = False
            item[1]["value"] = 0 if item[1]["type"] == "int" else ""
        structure = {"config": config}
        with open(config_file, "w") as f:
            json.dump(structure, f, indent=4)
        print("Конфигурация сброшена.")

    edit_menu = Menu(name="Редактирование")
    for key in config:
        edit_menu.add_item(text="Изменить " + key, function=get_property_editor(key))

    menu = Menu(name="Операции над " + config_file)
    menu.add_item(text="Узнать состояние", function=get_condition)
    menu.add_item(text="Вывести содержимое", function=print_contents)
    menu.add_item(text="Обнулить", function=reset_config)
    menu.add_item(submenu=edit_menu)
    return menu
