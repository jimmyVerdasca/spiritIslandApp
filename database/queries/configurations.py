def get_all(cursor):

    cursor.execute(
        """
        SELECT
            id,
            name,
            min_players,
            max_players

        FROM board_configurations

        ORDER BY min_players
        """
    )

    return cursor.fetchall()



def get_for_players(cursor, players):

    cursor.execute(
        """
        SELECT
            id,
            name,
            min_players,
            max_players

        FROM board_configurations

        WHERE ?
        BETWEEN min_players
        AND max_players
        """,
        (players,)
    )

    return cursor.fetchall()



def get_by_name(cursor, name):

    cursor.execute(
        """
        SELECT
            id,
            name,
            min_players,
            max_players

        FROM board_configurations

        WHERE name = ?
        """,
        (name,)
    )

    return cursor.fetchone()