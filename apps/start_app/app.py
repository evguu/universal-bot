from apps.apps_router import command_route


@command_route(commands=["/start", "начать", "пачаць", "start"],
               args=["server", "req"],
               help_text="Команда для вывода приветствия.")
def execute(server, req):
    server.send_message(req.user, "Дароу, тут будет вступление, а пока что тут я")
