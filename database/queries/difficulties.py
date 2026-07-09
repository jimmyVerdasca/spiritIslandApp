def get_all(cursor):

    cursor.execute(
        """
        SELECT id, level
        FROM difficulties
        ORDER BY level
        """
    )

    return cursor.fetchall()



def get_by_level(cursor, level):

    cursor.execute(
        """
        SELECT id, level
        FROM difficulties
        WHERE level = ?
        """,
        (level,)
    )

    return cursor.fetchone()