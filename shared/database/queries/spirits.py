GET_ALL = """
    SELECT
        id,
        key

    FROM spirits

    ORDER BY key
"""


GET_BY_KEY = """
    SELECT
        id,
        key

    FROM spirits

    WHERE key = ?
"""


GET_BY_GAME_ID = """
    SELECT
        s.id,
        s.key

    FROM spirits s

    JOIN game_spirits gs
        ON gs.spirit_id = s.id

    WHERE gs.game_id = ?

    ORDER BY gs.position
"""