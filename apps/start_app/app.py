from apps.apps_router import command_route


@command_route(commands=["/start", "начать", "пачаць", "start"],
               args=["server", "req"],
               help_text="Команда для вывода приветствия.")
def _(server, req):
    server.send_message(req.user, "Привет, я Хранитель Запретов!\nВерсия: 1.3\n\n"
                                  "Воспользуйся /help, чтобы получить список доступных тебе команд.\n"
                                  "Некоторые команды доступны только при наличии определенных прав, "
                                  "и ты увидишь их только если получишь эти самые права.\n"
                                  "Свои пожелания и предложения по работе бота присылайте через команду /feedback.\n\n"
                                  "Помните, что за чрезмерный флуд некоторыми командами (например /feedback) "
                                  "можно получить запрет на использование бота в течение некоторого "
                                  "промежутка времени.\n\n"
                                  "Приятного использования!")
