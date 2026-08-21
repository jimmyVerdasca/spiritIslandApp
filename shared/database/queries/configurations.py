from shared.models.game import BoardConfiguration
from shared.models.converters import row_to_configuration


def get_all(cursor) -> list[BoardConfiguration]:

    cursor.execute(
        """
        SELECT
            id,
            key,
            min_players,
            max_players

        FROM board_configurations

        ORDER BY min_players
        """
    )

    return [
        row_to_configuration(row)
        for row in cursor.fetchall()
    ]


def get_for_players(
    cursor,
    players
) -> list[BoardConfiguration]:

    cursor.execute(
        """
        SELECT
            id,
            key,
            min_players,
            max_players

        FROM board_configurations

        WHERE ?
        BETWEEN min_players
        AND max_players
        """,
        (players,)
    )

    return [
        row_to_configuration(row)
        for row in cursor.fetchall()
    ]


def get_by_key(
    cursor,
    key
) -> BoardConfiguration:

    cursor.execute(
        """
        SELECT
            id,
            key,
            min_players,
            max_players

        FROM board_configurations

        WHERE key = ?
        """,
        (key,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Configuration not found: {key}"
        )

    return row_to_configuration(row)


def get_by_id(
    cursor,
    configuration_id
) -> BoardConfiguration:

    cursor.execute(
        """
        SELECT
            id,
            key,
            min_players,
            max_players

        FROM board_configurations

        WHERE id = ?
        """,
        (configuration_id,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Configuration not found: {configuration_id}"
        )

    return row_to_configuration(row)