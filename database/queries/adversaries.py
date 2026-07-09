import random


def get_all(cursor):

    cursor.execute(
        """
        SELECT id, name
        FROM adversaries
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
        FROM adversaries
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    return cursor.fetchone()



def get_by_name(cursor, name):

    cursor.execute(
        """
        SELECT id, name
        FROM adversaries
        WHERE name = ?
        """,
        (name,)
    )

    return cursor.fetchone()