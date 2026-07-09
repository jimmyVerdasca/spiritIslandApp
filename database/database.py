import sqlite3
from pathlib import Path
from kivy.resources import resource_find


DB_NAME = "spirit_island.db"


def get_database_path():

    path = resource_find(
        "database/" + DB_NAME
    )

    return path


def get_connection():
    return sqlite3.connect(
        get_database_path()
    )