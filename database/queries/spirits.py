from database.database import get_connection
import random

def get_all(cursor):

    cursor.execute(
        """
        SELECT id, name
        FROM spirits
        ORDER BY name
        """
    )

    spirits = cursor.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in spirits
    ]


def get_random(cursor, count):

    spirits = get_all(cursor)

    return random.sample(
        spirits,
        count
    )