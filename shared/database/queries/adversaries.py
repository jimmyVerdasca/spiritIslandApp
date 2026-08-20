from shared.models.game import Adversary, GameAdversary
from shared.models.converters import (
    row_to_adversary,
    row_to_game_adversary,
)


def get_all(cursor) -> list[Adversary]:

    cursor.execute(
        """
        SELECT id, key
        FROM adversaries
        ORDER BY key
        """
    )

    return [
        row_to_adversary(row)
        for row in cursor.fetchall()
    ]


def get_random(cursor) -> Adversary:

    cursor.execute(
        """
        SELECT id, key
        FROM adversaries
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    return row_to_adversary(
        cursor.fetchone()
    )


def get_by_key(cursor, key) -> Adversary:

    cursor.execute(
        """
        SELECT id, key
        FROM adversaries
        WHERE key = ?
        """,
        (key,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Adversary not found: {key}"
        )

    return row_to_adversary(row)


def get_by_id(cursor, game_id) -> list[GameAdversary]:
    
    cursor.execute(
        """
        SELECT
            a.id AS adversary_id,
            a.key AS adversary_key,

            d.id AS difficulty_id,
            d.level AS difficulty_level,

            ad.score_difficulty AS score_difficulty

        FROM game_adversaries ga

        JOIN adversaries a
            ON a.id = ga.adversary_id

        JOIN difficulties d
            ON d.id = ga.difficulty_id

        JOIN adversary_difficulties ad
            ON ad.adversary_id = a.id
            AND ad.difficulty_id = d.id

        WHERE ga.game_id = ?

        ORDER BY ga.adversary_id
        """,
        (game_id,)
    )

    return [
        row_to_game_adversary(row)
        for row in cursor.fetchall()
    ]