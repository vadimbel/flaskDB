from flask import g
import sqlite3


def connect_db():
    """
    Create connection with sqlite
    :return: sqlite connection
    """
    sql = sqlite3.connect('C:\\Users\\vadim\PycharmProjects\\shopping\\users.db')
    return sql


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def add_item(username: str, password: str, db):
    """
    Add new item to sqlite 'users' table
    :param username: username
    :param password: password
    :param db: sqlite connection
    :return:
    """
    db.execute(f"INSERT INTO users (username, password) VALUES (?, ?)", [username, password])
    db.commit()


def get_item(username: str, password:str, db):
    """
    Get all data from 'users' sqlite table
    :param username: username
    :param password: password
    :param db: sqlite connection
    :return:
    """
    return db.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'").fetchall()


def delete_item(username: str, db):
    """
    Delete item from 'users' table sqlite table
    :param username: username
    :param db: sqlite connection
    :return:
    """
    db.execute(f"DELETE FROM users WHERE username='{username}'")
    db.commit()


def check_both_fields(username, password):
    """
    Check if both text-fileds on 'main_page' are not empty
    :param username: username
    :param password: password
    :return:
    """
    if len(username) == 0 or len(password) == 0:
        return False

    return True


def check_username(username, db):
    """
    Check if provided username is in db
    :param username: username
    :param db: sqlite connection
    :return:
    """
    res = db.execute("SELECT username FROM users").fetchall()

    for un in res:
        if username == un[0]:
            return False

    return True


def check_username_in_db(username, db):
    """
    Check if provided username is not in db
    :param username: username
    :param db: sqlite connection
    :return:
    """
    return not check_username(username, db)
