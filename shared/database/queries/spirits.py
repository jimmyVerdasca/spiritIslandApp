import random

from shared.models.game import Spirit
from shared.models.converters import row_to_spirit


def get_all(cursor) -> list[Spirit]:

    cursor.execute(
        """
        SELECT
            id,
            key

        FROM spirits

        ORDER BY key
        """
    )

    return [
        row_to_spirit(row)
        for row in cursor.fetchall()
    ]


def get_random(
    cursor,
    count
) -> list[Spirit]:

    spirits = get_all(cursor)

    return random.sample(
        spirits,
        count
    )


def get_by_key(
    cursor,
    key
) -> Spirit:

    cursor.execute(
        """
        SELECT
            id,
            key

        FROM spirits

        WHERE key = ?
        """,
        (key,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Spirit not found: {key}"
        )

    return row_to_spirit(row)


def get_by_id(
    cursor,
    game_id
) -> list[Spirit]:

    cursor.execute(
        """
        SELECT
            s.id,
            s.key

        FROM spirits s

        JOIN game_spirits gs
            ON gs.spirit_id = s.id

        WHERE gs.game_id = ?

        ORDER BY gs.position
        """,
        (game_id,)
    )

    return [
        row_to_spirit(row)
        for row in cursor.fetchall()
    ]