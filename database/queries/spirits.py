import random

from models.game import Spirit
from models.converters import row_to_spirit


def get_all(cursor) -> list[Spirit]:

    cursor.execute(
        """
        SELECT id, name
        FROM spirits
        ORDER BY name
        """
    )

    return [
        row_to_spirit(row)
        for row in cursor.fetchall()
    ]


def get_random(cursor, count) -> list[Spirit]:

    spirits = get_all(cursor)

    return random.sample(
        spirits,
        count
    )


def get_by_name(cursor, name) -> Spirit:

    cursor.execute(
        """
        SELECT id, name
        FROM spirits
        WHERE name = ?
        """,
        (name,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Spirit not found: {name}"
        )

    return row_to_spirit(row)

def get_by_id(cursor, game_id):
    
    cursor.execute(
        """
        SELECT
            s.id,
            s.name

        FROM spirits s

        JOIN game_spirits gs
            ON gs.spirit_id = s.id

        WHERE gs.game_id = ?

        ORDER BY gs.position
        """,
        (game_id,)
    )

    return cursor.fetchall()