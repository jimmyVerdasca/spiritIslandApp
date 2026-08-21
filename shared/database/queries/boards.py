import random

from shared.models.game import Board, BoardConfiguration
from shared.models.converters import (
    row_to_board,
    row_to_configuration,
)


# =========================================================
# BOARDS
# =========================================================

def get_all(cursor) -> list[Board]:

    cursor.execute(
        """
        SELECT id, key
        FROM boards
        ORDER BY key
        """
    )

    return [
        row_to_board(row)
        for row in cursor.fetchall()
    ]


def get_by_key(cursor, key) -> Board:

    cursor.execute(
        """
        SELECT id, key
        FROM boards
        WHERE key = ?
        """,
        (key,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Board not found: {key}"
        )

    return row_to_board(row)


def get_for_game(cursor, game_id) -> list[Board]:

    cursor.execute(
        """
        SELECT
            b.id,
            b.key

        FROM boards b

        JOIN game_boards gb
            ON gb.board_id = b.id

        WHERE gb.game_id = ?

        ORDER BY gb.position
        """,
        (game_id,)
    )

    return [
        row_to_board(row)
        for row in cursor.fetchall()
    ]


def get_key(cursor, board_id) -> str:

    cursor.execute(
        """
        SELECT key
        FROM boards
        WHERE id = ?
        """,
        (board_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Board id not found: {board_id}"
        )

    return row["key"]


# =========================================================
# BOARD CONFIGURATION
# =========================================================

def get_configuration(
    cursor,
    key=None,
    players=None,
) -> BoardConfiguration:

    if key:

        cursor.execute(
            """
            SELECT
                id,
                key,
                min_players,
                max_players

            FROM board_configurations

            WHERE key = ?
            """,
            (key,)
        )

    elif players is not None:

        cursor.execute(
            """
            SELECT
                id,
                key,
                min_players,
                max_players

            FROM board_configurations

            WHERE min_players <= ?
            AND max_players >= ?
            """,
            (
                players,
                players,
            )
        )

    else:

        cursor.execute(
            """
            SELECT
                id,
                key,
                min_players,
                max_players

            FROM board_configurations
            """
        )

    rows = cursor.fetchall()

    if not rows:

        raise Exception(
            "No compatible board configuration"
        )

    return row_to_configuration(
        random.choice(rows)
    )


# =========================================================
# RANDOM BOARDS
# =========================================================

def get_random_boards(
    cursor,
    available: list[Board],
    quantity: int,
) -> list[Board]:

    return random.sample(
        available,
        quantity,
    )