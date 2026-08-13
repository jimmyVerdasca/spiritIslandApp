from models.converters import row_to_adversary_difficulty


def get_adversary_difficulty(
    cursor,
    adversary_id,
    difficulty_id,
):

    cursor.execute(
        """
        SELECT
            a.id AS adversary_id,
            a.key AS adversary_key,

            d.id AS difficulty_id,
            d.level AS difficulty_level,

            ad.score_difficulty

        FROM adversary_difficulties ad

        JOIN adversaries a
            ON a.id = ad.adversary_id

        JOIN difficulties d
            ON d.id = ad.difficulty_id

        WHERE ad.adversary_id = ?
        AND ad.difficulty_id = ?
        """,
        (
            adversary_id,
            difficulty_id,
        )
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return row_to_adversary_difficulty(row)