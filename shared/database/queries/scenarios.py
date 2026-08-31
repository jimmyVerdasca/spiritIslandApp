GET_ALL = """
    SELECT
        id,
        key,
        score_difficulty

    FROM scenarios

    ORDER BY key
"""


GET_RANDOM = """
    SELECT
        id,
        key,
        score_difficulty

    FROM scenarios

    ORDER BY RANDOM()

    LIMIT 1
"""


GET_BY_KEY = """
    SELECT
        id,
        key,
        score_difficulty

    FROM scenarios

    WHERE key = ?
"""


GET_BY_GAME_ID = """
    SELECT
        s.id,
        s.key,
        s.score_difficulty

    FROM scenarios s

    JOIN game_scenarios gs
        ON gs.scenario_id = s.id

    WHERE gs.game_id = ?
"""


GET_BY_ID = """
    SELECT
        id,
        key,
        score_difficulty

    FROM scenarios

    WHERE id = ?
"""