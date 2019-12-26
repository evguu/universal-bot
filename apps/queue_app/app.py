from utils.hookers import Hooker, HookerArgData, HookerArgPathway
import pickle
import random
from apps.queue_app import config
from apps.apps_router import command_route

users_972304 = [
    ['А. Крепец', 1],
    ['А. Бутько', 1],
    ['В. Лопуть', 1],
    ['В. Бесараб', 1],
    ['В. Минько', 1],
    ['В. Бань', 1],
    ['В. Боровой', 1],
    ['Е. Дольский', 1],
    ['И. Гора', 1],
    ['И. Ковальчук', 1],
    ['М. Борисюк', 1],
    ['М. Кардаш', 1],
    ['Н. Кабак', 1],
    ['С. Кухарева', 1],
    ['Я. Волкова', 1],
    ['А. Петлицкий', 2],
    ['В. Мокийчук', 2],
    ['Д. Шишко', 2],
    ['Е. Савченко', 2],
    ['И. Некрашевич', 2],
    ['И. Селявко', 2],
    ['И. Терлецкий', 2],
    ['К. Кукурузов', 2],
    ['Л. Снопок', 2],
    ['М. Синькевич', 2],
    ['М. Кукурузова', 2],
    ['М. Хвесько', 2],
    ['Н. Приходовская', 2],
    ['П. Кукурузов', 2],
    ['Р. Дурдыев', 2],
    ['С. Хоров', 2],
]

users = {
    "1": [user for user in users_972304 if user[1] == 1],
    "2": [user for user in users_972304 if user[1] == 2]
}

users_random_map = {}
for i in users:
    users_random_map[i] = {}


def randomize_users():
    global users, users_random_map
    available_slots = {}
    for i in users:
        available_slots[i] = [j + 1 for j in range(len(users[i]))]
    for i in users:
        for key in users[i]:
            given_slot = random.choice(available_slots[i])
            available_slots[i].remove(given_slot)
            users_random_map[i][key[0]] = given_slot


def get_users_list(subgroup):
    res = list(users_random_map[subgroup].items())
    res.sort(key=lambda x: x[1])
    return "\n".join(["{1}: {0}".format(*i) for i in res])


def save_randomized():
    with open(config.randomized_table_file, 'wb+') as f:
        pickle.dump(users_random_map, f)


def load_randomized():
    global users_random_map
    with open(config.randomized_table_file, 'rb') as f:
        users_random_map = pickle.load(f)


def get_user(subgroup, name):
    load_randomized()
    if name in users_random_map[subgroup]:
        return "Номер студента {}: {}.".format(name,
                                               users_random_map[subgroup][name])
    else:
        return "Такого имени не найдено в этой подгруппе."


@command_route(commands=["/random"],
               args=["req", "args"],
               help_text="Узнать свой номер в очереди.")
def execute(req, args):
    def hooker_done(subgroup, name):
        return get_user(subgroup, name)

    def arg1_validator(x):
        return x in "12"
    subgroup_pathway = HookerArgPathway([
        (
            HookerArgData(lambda x: True,
                          "Выберите имя (подгруппа 1)",
                          options=[["{}".format(user[0])]
                                   for user in users["1"]]),
            lambda x: x[-1] == "1"
        ),
        (
            HookerArgData(lambda x: True,
                          "Выберите имя (подгруппа 2)",
                          options=[["{}".format(user[0])]
                                   for user in users["2"]]),
            lambda x: x[-1] == "2"
        )
    ])
    print(users)
    hooker = Hooker(req.user, hooker_done,
                    HookerArgData(arg1_validator,
                                  "Ваша подгруппа?",
                                  options=[["1"], ["2"]]),
                    subgroup_pathway)
    if len(args):
        try:
            hooker_response = hooker.arg_read(args[0], message_id=req.message_id, presend=True)
        except AttributeError:
            hooker_response = hooker.arg_read(args[0], presend=True)
        args.pop(0)
        if not hooker_response:
            return
    if len(args):
        try:
            hooker_response = hooker.arg_read(" ".join(args), message_id=req.message_id, presend=True)
        except AttributeError:
            hooker_response = hooker.arg_read(" ".join(args), presend=True)
        if not hooker_response:
            return
    hooker.init(getattr(req, "message_id", None))


def get_972304_list():
    load_randomized()
    return "Подгруппа 1:\n" \
           "{}\n" \
           "\n" \
           "Подгруппа 2:\n" \
           "{}".format(get_users_list("1"),
                       get_users_list("2"))


@command_route(commands=["/list"],
               args=["server", "req"],
               help_text="Вывести всю очередь.")
def execute(server, req):
    server.send_message(req.user, "Список студентов группы 972304 в порядке очередности:\n"
                                  "\n" + get_972304_list())
