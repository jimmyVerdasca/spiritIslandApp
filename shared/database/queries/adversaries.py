# =========================================================
# ALL ADVERSARIES
# =========================================================

GET_ALL = """
    SELECT
        id,
        key
    FROM adversaries
    ORDER BY key
"""


# =========================================================
# RANDOM ADVERSARY
# =========================================================

GET_RANDOM = """
    SELECT
        id,
        key
    FROM adversaries
    ORDER BY RANDOM()
    LIMIT 1
"""


# =========================================================
# ADVERSARY BY KEY
# =========================================================

GET_BY_KEY = """
    SELECT
        id,
        key
    FROM adversaries
    WHERE key = ?
"""


# =========================================================
# ADVERSARIES FOR GAME
# =========================================================

GET_BY_GAME_ID = """
    SELECT
        a.id AS adversary_id,
        a.key AS adversary_key,

        d.id AS difficulty_id,
        d.level AS difficulty_level,

        ad.score_difficulty AS score_difficulty

    FROM game_adversaries ga

    JOIN adversaries a
        ON a.id = ga.adversary_id

    JOIN difficulties d
        ON d.id = ga.difficulty_id

    JOIN adversary_difficulties ad
        ON ad.adversary_id = a.id
        AND ad.difficulty_id = d.id

    WHERE ga.game_id = ?

    ORDER BY ga.adversary_id
"""