"""
Группы представляют собой лист прав. Для выполнения команды нужно иметь все права, которые она требует.
"""


def is_valid_right_name(name):
    alphabet = "0123456789qwertyuiopasdfghjklzxcvbnm_"
    return all([i in alphabet for i in name])


def has_permission(perm_list, requirement):
    """
    Имеются ли все необходимые права у группы?
    """
    return all(elem in perm_list for elem in requirement)


def perm(permissions, extends=None):
    """
    Создать группу (в том числе на основе другой группы)
    """
    if extends:
        return extends.copy() + permissions
    else:
        return permissions


def str_perm(permissions):
    """
    Преобразовать группу в строку
    """
    return ";".join(permissions)


def destr_perm(string):
    """
    Создать группу из строки
    """
    return string.split(";")


def add_right(group, right):
    if right not in group:
        group.append(right)


def remove_right(group, right):
    if right in group:
        group.pop(group.index(right))


permissionNone = perm([])
permissionBasic = perm(["Basic"])
permissionVIP = perm(["VIP"], extends=permissionBasic)
permissionOwner = perm(["Owner"], extends=permissionVIP)
