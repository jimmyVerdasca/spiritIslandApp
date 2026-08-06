from pathlib import Path
import shutil
import sqlite3
from . import queries
from models.game_status import GameStatus
from models.game import Game
from models.converters import row_to_game, row_to_adversary, row_to_board, row_to_scenario, row_to_spirit, row_to_game_adversary, row_to_configuration

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

def get_connection(row_factory=True):
    path = get_database_path()
    print(f"Database path: {path}")

    db = sqlite3.connect(path)

    if row_factory:
        db.row_factory = sqlite3.Row

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

def save_game(game: Game) -> int:
    
    db = get_connection()

    try:
        cursor = db.cursor()

        game_id = queries.games.save_game(
            cursor,
            game
        )

        db.commit()

        return game_id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_running_games(limit=20, offset=0) -> list[Game]:
    
    db = get_connection()

    try:
        cursor = db.cursor()

        rows = queries.games.get_by_status(
            cursor,
            GameStatus.RUNNING,
            limit,
            offset
        )

        games = []

        for row in rows:
            print("GAME DB ROW:", dict(row))

            game = row_to_game(row)

            game.configuration = queries.configurations.get_by_name(
                    cursor,
                    game.configuration
                )

            game.spirits = [
                row_to_spirit(r)
                for r in queries.spirits.get_by_id(
                    cursor,
                    game.id
                )
            ]

            game.boards = [
                row_to_board(r)
                for r in queries.boards.get_by_id(
                    cursor,
                    game.id
                )
            ]

            game.adversaries = [
                row_to_game_adversary(r)
                for r in queries.adversaries.get_by_id(
                    cursor,
                    game.id
                )
            ]

            game.scenarios = [
                row_to_scenario(r)
                for r in queries.scenarios.get_by_id(
                    cursor,
                    game.id
                )
            ]

            games.append(game)

        return games

    finally:
        db.close()

def get_configurations():
    db = get_connection()
    
    try:
        cursor = db.cursor()

        configurations = queries.configurations.get_all(
            cursor
        )

        return configurations

    finally:
        db.close()

def get_spirits():
    db = get_connection()
    
    try:
        cursor = db.cursor()

        spirits = queries.spirits.get_all(
            cursor
        )

        return spirits

    finally:
        db.close()

def get_boards():
    db = get_connection()
    
    try:
        cursor = db.cursor()

        boards = queries.boards.get_all(
            cursor
        )

        return boards

    finally:
        db.close()

def get_adversaries():
    db = get_connection()
    
    try:
        cursor = db.cursor()

        adversaries = queries.adversaries.get_all(
            cursor
        )

        return adversaries

    finally:
        db.close()

def get_difficulties():
    db = get_connection()
    
    try:
        cursor = db.cursor()

        difficulties = queries.difficulties.get_all(
            cursor
        )

        return difficulties

    finally:
        db.close()

def get_scenarios():
    db = get_connection()
    
    try:
        cursor = db.cursor()

        scenarios = queries.scenarios.get_all(
            cursor
        )

        return scenarios

    finally:
        db.close()