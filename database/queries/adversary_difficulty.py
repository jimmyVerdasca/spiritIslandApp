from models.converters import row_to_adversary_difficulty

def get_all(cursor):
    
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

        ORDER BY
            ad.adversary_id,
            ad.difficulty_id
        """
    )

    return [
        row_to_adversary_difficulty(row)
        for row in cursor.fetchall()
    ]