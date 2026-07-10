from pathlib import Path
import shutil
import sqlite3

from contextlib import contextmanager

from kivy.app import App

from database.config import (
    DB_NAME,
    DATABASE_VERSION,
    DB_PATH
)


def get_database_path():

    app = App.get_running_app()

    if app is None:
        raise RuntimeError(
            "Kivy application is not running"
        )


    data_dir = Path(
        app.user_data_dir
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    target = data_dir / DB_NAME


    if needs_database_update(target):

        install_database(target)


    return target



def needs_database_update(target):

    # First installation
    if not target.exists():
        return True


    try:

        db = sqlite3.connect(target)

        cursor = db.cursor()

        cursor.execute(
            """
            SELECT version
            FROM database_info
            """
        )

        version = cursor.fetchone()[0]

        db.close()


        print(
            "Database version:",
            version,
            "Required:",
            DATABASE_VERSION
        )

        return version != DATABASE_VERSION


    except Exception:

        # Database corrupted or old format
        return True


def install_database(target):
    
    source = DB_PATH

    if source is None:

        raise FileNotFoundError(
            "Bundled database not found"
        )


    shutil.copyfile(
        source,
        target
    )


@contextmanager
def database():

    connection = get_connection()

    try:
        yield connection

    finally:
        connection.close()

def get_connection():
    path = get_database_path()
    print(f"Database path: {path}")

    db = sqlite3.connect(path)

    cursor = db.cursor()

    cursor.execute("PRAGMA user_version")
    version = cursor.fetchone()[0]

    print(f"Database version: {version}")

    if version != DATABASE_VERSION:
        print("WARNING: database version mismatch!")
        print(f"Expected: {DATABASE_VERSION}")
        print(f"Found:    {version}")

    else:
        print("Database version OK")

    return db