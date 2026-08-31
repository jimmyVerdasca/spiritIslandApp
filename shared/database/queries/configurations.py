GET_ALL = """
    SELECT
        id,
        key,
        min_players,
        max_players

    FROM board_configurations

    ORDER BY min_players
"""


GET_FOR_PLAYERS = """
    SELECT
        id,
        key,
        min_players,
        max_players

    FROM board_configurations

    WHERE ?
    BETWEEN min_players
    AND max_players
"""


GET_BY_KEY = """
    SELECT
        id,
        key,
        min_players,
        max_players

    FROM board_configurations

    WHERE key = ?
"""


GET_BY_ID = """
    SELECT
        id,
        key,
        min_players,
        max_players

    FROM board_configurations

    WHERE id = ?
"""