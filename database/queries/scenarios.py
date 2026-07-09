def get_all(cursor):

    cursor.execute(
        """
        SELECT id, name
        FROM scenarios
        ORDER BY name
        """
    )

    return [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in cursor.fetchall()
    ]



def get_random(cursor):

    cursor.execute(
        """
        SELECT id, name
        FROM scenarios
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    return cursor.fetchone()



def get_by_name(cursor, name):

    cursor.execute(
        """
        SELECT id, name
        FROM scenarios
        WHERE name = ?
        """,
        (name,)
    )

    return cursor.fetchone()