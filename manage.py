import os

from apps.queue_app.app import get_972304_list
from apps.queue_app.rerandomize import rerandomize
from servers.Telegram import webhook_manage
from utils.config_edit import get_editing_menu_for_config
from utils.console_menu import Menu

directory = os.path.dirname(__file__)

bind_menu = Menu("Привязка")
bind_menu.add_item(text="Telegram", function=webhook_manage.main)

queue_menu = Menu("Приложение: Очереди")
queue_menu.add_item(text="Перерандом", function=rerandomize)
queue_menu.add_item(text="Вывести очередь", function=lambda: print(get_972304_list()))

global_config_path = os.path.join(directory, "config", "config.json")
global_config_edit_menu = get_editing_menu_for_config(global_config_path)
telegram_config_path = os.path.join(directory, "servers", "Telegram", "config.json")
telegram_config_edit_menu = get_editing_menu_for_config(telegram_config_path)
vk_config_path = os.path.join(directory, "servers", "VK", "config.json")
vk_config_edit_menu = get_editing_menu_for_config(vk_config_path)

config_hub = Menu("Конфигурация")
config_hub.add_item(submenu=global_config_edit_menu)
config_hub.add_item(submenu=telegram_config_edit_menu)
config_hub.add_item(submenu=vk_config_edit_menu)

main_menu = Menu("Управление")
main_menu.add_item(submenu=bind_menu)
main_menu.add_item(submenu=queue_menu)
main_menu.add_item(submenu=config_hub)
main_menu.add_item(text="Выход", function=exit)

main_menu.set_main()


def main():
    is_running = True
    while is_running:
        active_menu = Menu.get_active_menu()
        active_menu.print()
        choice = input()
        active_menu.press_item(choice)


if __name__ == '__main__':
    main()
