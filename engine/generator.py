from database.database import get_connection


def generate_game(
    players=None,
    max_difficulty=None
):

    db = get_connection()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT name
        FROM spirits
        LIMIT 5
        """
    )


    spirits = cursor.fetchall()


    db.close()


    return {
        "players": players,
        "max_difficulty": max_difficulty,
        "spirits": spirits
    }