from pathlib import Path
import shutil
import sqlite3
from contextlib import contextmanager

from kivy.app import App

from . import queries
from database.migrations.runner import run_migrations

from models.game_status import GameStatus
from models.game import Game
from models.converters import row_to_game

from engine.trophy_conditions import CONDITIONS

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

    if not target.exists():
        install_database(target)
    else:
        run_migrations(target)

    return target


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

    print(
        f"Database path: {path}"
    )

    db = sqlite3.connect(path)

    if row_factory:
        db.row_factory = sqlite3.Row

    cursor = db.cursor()

    cursor.execute(
        "PRAGMA user_version"
    )

    version = cursor.fetchone()[0]

    print(
        f"Database version: {version}"
    )

    if version != DATABASE_VERSION:

        print(
            "WARNING: database version mismatch!"
        )

        print(
            f"Expected: {DATABASE_VERSION}"
        )

        print(
            f"Found:    {version}"
        )

    else:

        print(
            "Database version OK"
        )

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


def _get_games_by_status(
    status: GameStatus,
    result=None,
    limit=20,
    offset=0
) -> list[Game]:

    db = get_connection()

    try:

        cursor = db.cursor()

        rows = queries.games.get_by_status(
            cursor,
            status,
            result,
            limit,
            offset
        )

        games = []

        for row in rows:

            game = row_to_game(row)

            game.configuration = (
                queries.configurations.get_by_key(
                    cursor,
                    game.configuration
                )
            )

            game.spirits = (
                queries.spirits.get_by_id(
                    cursor,
                    game.id
                )
            )

            game.boards = (
                queries.boards.get_for_game(
                    cursor,
                    game.id
                )
            )

            game.adversaries = (
                queries.adversaries.get_by_id(
                    cursor,
                    game.id
                )
            )

            game.scenarios = (
                queries.scenarios.get_by_id(
                    cursor,
                    game.id
                )
            )

            games.append(game)

        return games

    finally:

        db.close()


def get_running_games(
    limit=20,
    offset=0
) -> list[Game]:

    return _get_games_by_status(
        GameStatus.RUNNING,
        limit=limit,
        offset=offset
    )


def get_finished_games(
    result=None,
    limit=20,
    offset=0
) -> list[Game]:

    return _get_games_by_status(
        GameStatus.FINISHED,
        result=result,
        limit=limit,
        offset=offset
    )


def get_abandoned_games(
    limit=20,
    offset=0
) -> list[Game]:

    return _get_games_by_status(
        GameStatus.ABANDONED,
        limit,
        offset
    )


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


def abandon_game(game_id):

    db = get_connection()

    try:

        cursor = db.cursor()

        queries.games.abandon_game(
            cursor,
            game_id
        )

        db.commit()

    finally:

        db.close()


def finish_game(
    game_id,
    result,
    score,
    invader_cards,
    dahan,
    blight
):

    db = get_connection()

    try:

        cursor = db.cursor()

        queries.games.finish_game(
            cursor,
            game_id,
            result,
            score,
            invader_cards,
            dahan,
            blight
        )

        db.commit()

    finally:

        db.close()


def get_adversary_difficulty(
    adversary_id,
    difficulty_id
):

    db = get_connection()

    try:

        cursor = db.cursor()

        adversary_difficulty = (
            queries.adversary_difficulty
            .get_adversary_difficulty(
                cursor,
                adversary_id,
                difficulty_id
            )
        )

        return adversary_difficulty

    finally:

        db.close()


def get_scenario_difficulty(
    scenario_id
):

    db = get_connection()

    try:

        cursor = db.cursor()

        scenario = (
            queries.scenarios.get_scenario_difficulty(
                cursor,
                scenario_id
            )
        )

        if scenario is None:
            return None

        return scenario.score_difficulty

    finally:

        db.close()


def get_trophies():

    db = get_connection()

    try:

        cursor = db.cursor()

        trophies = queries.trophies.get_all(
            cursor
        )

        for trophy in trophies:

            trophy.unlocked = check_trophy_condition(
                cursor,
                trophy
            )

        return trophies

    finally:

        db.close()


def check_trophy_condition(
    cursor,
    trophy
):

    if trophy.sql_condition:

        cursor.execute(
            trophy.sql_condition
        )

        return bool(
            cursor.fetchone()[0]
        )

    if trophy.python_condition:

        return check_python_condition(
            trophy.python_condition
        )

    return False


def check_python_condition(
    condition_name
):

    games = get_finished_games()

    condition = CONDITIONS.get(
        condition_name
    )

    if condition is None:
        return False

    return condition(games)