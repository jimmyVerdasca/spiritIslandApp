import shutil
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from shared.models.game_status import GameStatus
from shared.models.game import Game
from shared.models.converters import row_to_game
from shared.engine.trophy_conditions import CONDITIONS

from .config import DATABASE_VERSION
from . import queries
from .migrations.runner import run_migrations


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def ensure_database(
    database_path,
    template_path,
):

    database_path = Path(
        database_path
    )

    template_path = Path(
        template_path
    )

    # -----------------------------------------------------
    # First launch
    # -----------------------------------------------------

    if not database_path.exists():

        database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not template_path.exists():

            raise FileNotFoundError(
                f"Bundled database not found: "
                f"{template_path}"
            )

        shutil.copyfile(
            template_path,
            database_path,
        )

    # -----------------------------------------------------
    # Existing database
    # -----------------------------------------------------

    run_migrations(
        database_path
    )


# =========================================================
# CONNECTION
# =========================================================

def get_connection(
    database_path,
    row_factory=True,
):

    database_path = Path(
        database_path
    )

    db = sqlite3.connect(
        database_path
    )

    if row_factory:

        db.row_factory = sqlite3.Row

    cursor = db.cursor()

    cursor.execute(
        "PRAGMA user_version"
    )

    version = cursor.fetchone()[0]

    if version != DATABASE_VERSION:
        raise RuntimeError(
            f"Database version mismatch: "
            f"expected {DATABASE_VERSION}, "
            f"found {version}"
        )

    return db


@contextmanager
def database(
    database_path,
):

    connection = get_connection(
        database_path
    )

    try:

        yield connection

    finally:

        connection.close()


# =========================================================
# GAMES
# =========================================================

def save_game(
    database_path,
    game: Game,
) -> int:

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        game_id = queries.games.save_game(
            cursor,
            game,
        )

        db.commit()

        return game_id

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


def _get_games_by_status(
    database_path,
    status: GameStatus,
    result=None,
    limit=20,
    offset=0,
) -> list[Game]:

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        rows = queries.games.get_by_status(
            cursor,
            status,
            result,
            limit,
            offset,
        )

        games = []

        for row in rows:

            game = row_to_game(
                row
            )

            game.configuration = (
                queries.configurations.get_by_key(
                    cursor,
                    game.configuration,
                )
            )

            game.spirits = (
                queries.spirits.get_by_id(
                    cursor,
                    game.id,
                )
            )

            game.boards = (
                queries.boards.get_for_game(
                    cursor,
                    game.id,
                )
            )

            game.adversaries = (
                queries.adversaries.get_by_id(
                    cursor,
                    game.id,
                )
            )

            game.scenarios = (
                queries.scenarios.get_by_id(
                    cursor,
                    game.id,
                )
            )

            games.append(
                game
            )

        return games

    finally:

        db.close()


def get_running_games(
    database_path,
    limit=20,
    offset=0,
) -> list[Game]:

    return _get_games_by_status(
        database_path,
        GameStatus.RUNNING,
        limit=limit,
        offset=offset,
    )


def get_finished_games(
    database_path,
    result=None,
    limit=20,
    offset=0,
) -> list[Game]:

    return _get_games_by_status(
        database_path,
        GameStatus.FINISHED,
        result=result,
        limit=limit,
        offset=offset,
    )


def get_abandoned_games(
    database_path,
    limit=20,
    offset=0,
) -> list[Game]:

    return _get_games_by_status(
        database_path,
        GameStatus.ABANDONED,
        limit=limit,
        offset=offset,
    )


# =========================================================
# STATIC DATA
# =========================================================

def get_configurations(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        return queries.configurations.get_all(
            cursor
        )

    finally:

        db.close()


def get_spirits(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        return queries.spirits.get_all(
            cursor
        )

    finally:

        db.close()


def get_boards(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        return queries.boards.get_all(
            cursor
        )

    finally:

        db.close()


def get_adversaries(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        return queries.adversaries.get_all(
            cursor
        )

    finally:

        db.close()


def get_difficulties(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        return queries.difficulties.get_all(
            cursor
        )

    finally:

        db.close()


def get_scenarios(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        return queries.scenarios.get_all(
            cursor
        )

    finally:

        db.close()


def get_adversaries_difficulties(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        return (
            queries.adversary_difficulty.get_all(
                cursor
            )
        )

    finally:

        db.close()


def get_scenario_difficulty(
    database_path,
    scenario_id,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        scenario = (
            queries.scenarios
            .get_scenario_difficulty(
                cursor,
                scenario_id,
            )
        )

        if scenario is None:
            return None

        return scenario.score_difficulty

    finally:

        db.close()


# =========================================================
# GAME STATE
# =========================================================

def abandon_game(
    database_path,
    game_id,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        queries.games.abandon_game(
            cursor,
            game_id,
        )

        db.commit()

    finally:

        db.close()


def finish_game(
    database_path,
    game_id,
    result,
    score,
    invader_cards,
    dahan,
    blight,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        queries.games.finish_game(
            cursor,
            game_id,
            result,
            score,
            invader_cards,
            dahan,
            blight,
        )

        db.commit()

    finally:

        db.close()


# =========================================================
# TROPHIES
# =========================================================

def get_trophies(
    database_path,
):

    db = get_connection(
        database_path
    )

    try:

        cursor = db.cursor()

        trophies = queries.trophies.get_all(
            cursor
        )

        for trophy in trophies:

            trophy.unlocked = (
                check_trophy_condition(
                    cursor,
                    trophy,
                    database_path,
                )
            )

        return trophies

    finally:

        db.close()


def check_trophy_condition(
    cursor,
    trophy,
    database_path,
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
            trophy.python_condition,
            database_path,
        )

    return False


def check_python_condition(
    condition_name,
    database_path,
):

    games = get_finished_games(
        database_path
    )

    condition = CONDITIONS.get(
        condition_name
    )

    if condition is None:
        return False

    return condition(
        games
    )