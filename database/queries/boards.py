import random

from models.game import Board, BoardConfiguration
from models.converters import row_to_board, row_to_configuration


def get_all(cursor) -> list[Board]:

    cursor.execute(
        """
        SELECT id, name
        FROM boards
        ORDER BY name
        """
    )

    return [
        row_to_board(row)
        for row in cursor.fetchall()
    ]



def get_by_name(cursor, name) -> Board:

    cursor.execute(
        """
        SELECT id, name
        FROM boards
        WHERE name=?
        """,
        (name,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Board not found: {name}"
        )

    return row_to_board(row)

def get_by_id(cursor, game_id):
    
    cursor.execute(
        """
        SELECT
            b.id,
            b.name

        FROM boards b

        JOIN game_boards gb
            ON gb.board_id = b.id

        WHERE gb.game_id = ?

        ORDER BY gb.position
        """,
        (game_id,)
    )

    return cursor.fetchall()



def get_name(cursor, board_id) -> str:

    cursor.execute(
        """
        SELECT name
        FROM boards
        WHERE id=?
        """,
        (board_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Board id not found: {board_id}"
        )

    return row["name"]



def get_configuration(cursor, name=None, players=None) -> BoardConfiguration:
    print(name)
    print(players)
    
    if name:
    
        cursor.execute(
            """
            SELECT
                id,
                name,
                min_players,
                max_players
            FROM board_configurations
            WHERE name = ?
            """,
            (name,)
        )

    elif players is not None:

        cursor.execute(
            """
            SELECT
                id,
                name,
                min_players,
                max_players
            FROM board_configurations
            WHERE min_players <= ?
            AND max_players >= ?
            """,
            (
                players,
                players
            )
        )

    else:

        cursor.execute(
            """
            SELECT
                id,
                name,
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



def get_random_boards(
    cursor,
    available: list[Board],
    quantity: int
) -> list[Board]:

    return random.sample(
        available,
        quantity
    )