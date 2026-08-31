import shutil
from pathlib import Path

from shared.models.game_status import GameStatus
from shared.models.game import Game
from shared.models.converters import (
    row_to_game,
    row_to_configuration,
    row_to_spirit,
    row_to_board,
    row_to_adversary,
    row_to_scenario,
    row_to_adversary_difficulty,
    row_to_trophy,
)
from shared.engine.trophy_conditions import CONDITIONS

from .config import DATABASE_VERSION
from . import queries
from .migrations.runner import run_migrations


# =========================================================
# LOCAL DATABASE INITIALIZATION
# =========================================================


def ensure_database(
    database_path,
    template_path,
):
    """
    Ensure a local SQLite database exists and is migrated.

    This is SQLite/filesystem-specific and is used by
    SQLiteDataProvider.

    Remote D1 databases should have their own deployment
    and migration mechanism.
    """

    database_path = Path(
        database_path
    )

    template_path = Path(
        template_path
    )

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

    run_migrations(
        database_path
    )


# =========================================================
# DATABASE VERSION
# =========================================================


def validate_database_version(
    executor,
):
    """
    Validate the local SQLite database schema version.

    This is intentionally SQLite-specific.

    D1 should use a separate schema/version mechanism because
    PRAGMA user_version is not part of the portable SQL contract.
    """

    row = executor.fetchone(
        "PRAGMA user_version"
    )

    if row is None:

        raise RuntimeError(
            "Unable to determine database version"
        )

    version = row[0]

    if version != DATABASE_VERSION:

        raise RuntimeError(
            f"Database version mismatch: "
            f"expected {DATABASE_VERSION}, "
            f"found {version}"
        )


# =========================================================
# GAMES
# =========================================================


def save_game(
    executor,
    game: Game,
) -> int:
    """
    Save a complete game.

    The query modules contain only raw SQL. All model-to-row
    conversion and orchestration happens here.
    """

    try:

        # -------------------------------------------------
        # GAME
        # -------------------------------------------------

        row = executor.fetchone(
            queries.games.SAVE_GAME,
            (
                game.players,
                game.configuration.id,
                game.status.value,
            ),
        )

        if row is None:

            raise RuntimeError(
                "Failed to create game"
            )

        game_id = row["id"]

        # -------------------------------------------------
        # SPIRITS
        # -------------------------------------------------

        for position, spirit in enumerate(
            game.spirits,
            start=1,
        ):

            executor.execute(
                queries.games.SAVE_GAME_SPIRIT,
                (
                    game_id,
                    spirit.id,
                    position,
                ),
            )

        # -------------------------------------------------
        # BOARDS
        # -------------------------------------------------

        for position, board in enumerate(
            game.boards,
            start=1,
        ):

            executor.execute(
                queries.games.SAVE_GAME_BOARD,
                (
                    game_id,
                    board.id,
                    position,
                ),
            )

        # -------------------------------------------------
        # ADVERSARIES
        # -------------------------------------------------

        for game_adversary in game.adversaries:

            executor.execute(
                queries.games.SAVE_GAME_ADVERSARY,
                (
                    game_id,
                    game_adversary.adversary.id,
                    game_adversary.difficulty.id,
                ),
            )

        # -------------------------------------------------
        # SCENARIOS
        # -------------------------------------------------

        for scenario in game.scenarios:

            executor.execute(
                queries.games.SAVE_GAME_SCENARIO,
                (
                    game_id,
                    scenario.id,
                ),
            )

        executor.commit()

        return game_id

    except Exception:

        executor.rollback()

        raise


# =========================================================
# GET GAMES BY STATUS
# =========================================================


def _get_games_by_status(
    executor,
    status: GameStatus,
    result=None,
    limit=20,
    offset=0,
) -> list[Game]:

    params = [
        status.value,
        result,
        result,
        limit,
        offset,
    ]

    rows = executor.fetchall(
        queries.games.GET_BY_STATUS,
        params,
    )

    games = []

    for row in rows:

        game = row_to_game(
            row
        )

        # -------------------------------------------------
        # CONFIGURATION
        # -------------------------------------------------

        configuration_row = executor.fetchone(
            queries.configurations.GET_BY_KEY,
            (
                game.configuration,
            ),
        )

        if configuration_row is None:

            raise ValueError(
                f"Configuration not found: "
                f"{game.configuration}"
            )

        game.configuration = (
            row_to_configuration(
                configuration_row
            )
        )

        # -------------------------------------------------
        # SPIRITS
        # -------------------------------------------------

        game.spirits = [
            row_to_spirit(row)
            for row in executor.fetchall(
                queries.spirits.GET_BY_GAME_ID,
                (
                    game.id,
                ),
            )
        ]

        # -------------------------------------------------
        # BOARDS
        # -------------------------------------------------

        game.boards = [
            row_to_board(row)
            for row in executor.fetchall(
                queries.boards.GET_BY_GAME_ID,
                (
                    game.id,
                ),
            )
        ]

        # -------------------------------------------------
        # ADVERSARIES
        # -------------------------------------------------

        game.adversaries = [
            row_to_adversary(row)
            for row in executor.fetchall(
                queries.adversaries.GET_BY_GAME_ID,
                (
                    game.id,
                ),
            )
        ]

        # -------------------------------------------------
        # SCENARIOS
        # -------------------------------------------------

        game.scenarios = [
            row_to_scenario(row)
            for row in executor.fetchall(
                queries.scenarios.GET_BY_GAME_ID,
                (
                    game.id,
                ),
            )
        ]

        games.append(
            game
        )

    return games


def get_running_games(
    executor,
    limit=20,
    offset=0,
) -> list[Game]:

    return _get_games_by_status(
        executor,
        GameStatus.RUNNING,
        limit=limit,
        offset=offset,
    )


def get_finished_games(
    executor,
    result=None,
    limit=20,
    offset=0,
) -> list[Game]:

    return _get_games_by_status(
        executor,
        GameStatus.FINISHED,
        result=result,
        limit=limit,
        offset=offset,
    )


def get_abandoned_games(
    executor,
    limit=20,
    offset=0,
) -> list[Game]:

    return _get_games_by_status(
        executor,
        GameStatus.ABANDONED,
        limit=limit,
        offset=offset,
    )


# =========================================================
# STATIC DATA
# =========================================================


def get_configurations(
    executor,
):

    return [
        row_to_configuration(row)
        for row in executor.fetchall(
            queries.configurations.GET_ALL
        )
    ]


def get_spirits(
    executor,
):

    return [
        row_to_spirit(row)
        for row in executor.fetchall(
            queries.spirits.GET_ALL
        )
    ]


def get_boards(
    executor,
):

    return [
        row_to_board(row)
        for row in executor.fetchall(
            queries.boards.GET_ALL
        )
    ]


def get_adversaries(
    executor,
):

    return [
        row_to_adversary(row)
        for row in executor.fetchall(
            queries.adversaries.GET_ALL
        )
    ]


def get_difficulties(
    executor,
):

    from shared.models.converters import (
        row_to_difficulty,
    )

    return [
        row_to_difficulty(row)
        for row in executor.fetchall(
            queries.difficulties.GET_ALL
        )
    ]


def get_scenarios(
    executor,
):

    return [
        row_to_scenario(row)
        for row in executor.fetchall(
            queries.scenarios.GET_ALL
        )
    ]


def get_adversaries_difficulties(
    executor,
):

    return [
        row_to_adversary_difficulty(row)
        for row in executor.fetchall(
            queries.adversary_difficulty.GET_ALL
        )
    ]


def get_scenario_difficulty(
    executor,
    scenario_id,
):

    row = executor.fetchone(
        queries.scenarios.GET_SCENARIO_DIFFICULTY,
        (
            scenario_id,
        ),
    )

    if row is None:

        return None

    return row["score_difficulty"]


# =========================================================
# GAME STATE
# =========================================================


def abandon_game(
    executor,
    game_id,
):

    try:

        executor.execute(
            queries.games.ABANDON_GAME,
            (
                GameStatus.ABANDONED.value,
                game_id,
            ),
        )

        executor.commit()

    except Exception:

        executor.rollback()

        raise


def finish_game(
    executor,
    game_id,
    result,
    score,
    invader_cards,
    dahan,
    blight,
):

    try:

        executor.execute(
            queries.games.FINISH_GAME,
            (
                GameStatus.FINISHED.value,
                result,
                score,
                invader_cards,
                dahan,
                blight,
                game_id,
            ),
        )

        executor.commit()

    except Exception:

        executor.rollback()

        raise


# =========================================================
# TROPHIES
# =========================================================


def get_trophies(
    executor,
):

    trophies = [
        row_to_trophy(row)
        for row in executor.fetchall(
            queries.trophies.GET_ALL
        )
    ]

    for trophy in trophies:

        trophy.unlocked = (
            check_trophy_condition(
                executor,
                trophy,
            )
        )

    return trophies


def check_trophy_condition(
    executor,
    trophy,
):

    if trophy.sql_condition:

        row = executor.fetchone(
            trophy.sql_condition
        )

        if row is None:

            return False

        # Trophy SQL conditions are expected to return
        # a single boolean/integer result.
        return bool(
            row[0]
        )

    if trophy.python_condition:

        return check_python_condition(
            trophy.python_condition,
            executor,
        )

    return False


def check_python_condition(
    condition_name,
    executor,
):

    games = get_finished_games(
        executor
    )

    condition = CONDITIONS.get(
        condition_name
    )

    if condition is None:

        return False

    return condition(
        games
    )