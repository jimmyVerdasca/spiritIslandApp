from models.game import AdversaryDifficulty, Adversary, Difficulty
from models.converters import row_to_adversary_difficulty


def get_game_difficulty(cursor, game_id):

    cursor.execute(
        """
        SELECT
            a.id AS adversary_id,
            a.name AS adversary_name,

            d.id AS difficulty_id,
            d.level AS difficulty_level,

            ad.score_difficulty

        FROM game_adversaries ga

        JOIN adversaries a
            ON a.id = ga.adversary_id

        JOIN difficulties d
            ON d.id = ga.difficulty_id

        JOIN adversary_difficulties ad
            ON ad.adversary_id = ga.adversary_id
            AND ad.difficulty_id = ga.difficulty_id

        WHERE ga.game_id = ?

        """,
        (
            game_id,
        )
    )

    row = cursor.fetchone()


    if row is None:
        return None


    return row_to_adversary_difficulty(row)