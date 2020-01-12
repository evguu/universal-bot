import os
import sqlite3

from utils import permissions

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
INIT_PATH = os.path.join(os.path.dirname(__file__), 'createdb.query')
conn = sqlite3.connect(DEFAULT_PATH, check_same_thread=False)
cursor = conn.cursor()


def _init_db():
    """
    Инициализирует БД
    """
    with open(INIT_PATH, "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def _ensure_db_exists():
    """
    Проверяет, инициализирована ли БД, если нет — инициализирует
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


def add_record(server_user_id, banned_until, reason, perm_level):
    try:
        cursor.execute(
            "INSERT INTO users (server_user_id, banned_until, reason, permission_level) VALUES (?, ?, ?, ?);",
            (server_user_id, banned_until, reason, perm_level))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_record(server_user_id):
    cursor.execute("SELECT * FROM users WHERE server_user_id=?;", (server_user_id,))
    return cursor.fetchone()


def update_permission_record(perm_group, suid):
    cursor.execute("UPDATE users\nSET permission_level=?\nWHERE server_user_id=?;",
                   (permissions.str_perm(perm_group), suid))
    conn.commit()


def update_ban_record(until, reason, suid):
    cursor.execute("UPDATE users\nSET banned_until=?,\nreason=?\nWHERE server_user_id=?;",
                   (until, reason, suid))
    conn.commit()


_ensure_db_exists()
