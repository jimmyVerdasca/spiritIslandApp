import random


def get_all(cursor):
    cursor.execute(
        """
        SELECT id, name
        FROM boards
        """
    )

    return cursor.fetchall()



def get_id(cursor, name):

    cursor.execute(
        """
        SELECT id
        FROM boards
        WHERE name=?
        """,
        (name,)
    )

    result = cursor.fetchone()

    if not result:
        raise ValueError(
            f"Board not found: {name}"
        )

    return result[0]



def get_name(cursor, board_id):

    cursor.execute(
        """
        SELECT name
        FROM boards
        WHERE id=?
        """,
        (board_id,)
    )

    result = cursor.fetchone()

    if not result:
        raise ValueError(
            f"Board id not found: {board_id}"
        )

    return result[0]



def get_configuration(cursor, name=None, players=None):

    if name:

        cursor.execute(
            """
            SELECT id, name
            FROM board_configurations
            WHERE name=?
            AND min_players <= ?
            AND max_players >= ?
            """,
            (
                name,
                players,
                players
            )
        )

    else:

        cursor.execute(
            """
            SELECT id, name
            FROM board_configurations
            WHERE min_players <= ?
            AND max_players >= ?
            """,
            (
                players,
                players
            )
        )


    configurations = cursor.fetchall()

    if not configurations:
        raise Exception(
            "No compatible board configuration"
        )

    row = random.choice(configurations)
    return {
        "id": row[0],
        "name": row[1]
    }


def get_available_boards(cursor, configuration_id):

    cursor.execute(
        """
        SELECT 
            boards.id,
            boards.name
        FROM boards
        JOIN configuration_boards
            ON boards.id = configuration_boards.board_id
        WHERE configuration_boards.configuration_id=?
        """,
        (
            configuration_id,
        )
    )

    return [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in cursor.fetchall()
    ]



def get_random_boards(cursor, available, quantity):

    return random.sample(
        available,
        quantity
    )