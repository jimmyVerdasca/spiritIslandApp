from models.game import Adversary, GameAdversary
from models.converters import row_to_game_adversary, row_to_adversary


def get_all(cursor) -> list[Adversary]:

    cursor.execute(
        """
        SELECT id, name
        FROM adversaries
        ORDER BY name
        """
    )

    return [
        row_to_adversary(row)
        for row in cursor.fetchall()
    ]


def get_random(cursor) -> Adversary:

    cursor.execute(
        """
        SELECT id, name
        FROM adversaries
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    return row_to_adversary(
        cursor.fetchone()
    )


def get_by_name(cursor, name) -> Adversary:

    cursor.execute(
        """
        SELECT id, name
        FROM adversaries
        WHERE name = ?
        """,
        (name,)
    )

    return row_to_adversary(
        cursor.fetchone()
    )

def get_by_id(cursor, game_id):
    
    cursor.execute(
        """
        SELECT
            a.id,
            a.name,
            d.level AS difficulty

        FROM adversaries a

        JOIN game_adversaries ga
            ON ga.adversary_id = a.id

        JOIN difficulties d
            ON d.id = ga.difficulty_id

        WHERE ga.game_id = ?
        """,
        (game_id,)
    )

    return cursor.fetchall()