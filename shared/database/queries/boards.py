
# =========================================================
# BOARDS
# =========================================================

GET_ALL = """
    SELECT
        id,
        key

    FROM boards

    ORDER BY key
"""


GET_BY_KEY = """
    SELECT
        id,
        key

    FROM boards

    WHERE key = ?
"""


GET_FOR_GAME = """
    SELECT
        b.id,
        b.key

    FROM boards b

    JOIN game_boards gb
        ON gb.board_id = b.id

    WHERE gb.game_id = ?

    ORDER BY gb.position
"""


GET_KEY = """
    SELECT
        key

    FROM boards

    WHERE id = ?
"""


# =========================================================
# BOARD CONFIGURATION
# =========================================================

GET_CONFIGURATION_BY_KEY = """
    SELECT
        id,
        key,
        min_players,
        max_players

    FROM board_configurations

    WHERE key = ?
"""


GET_CONFIGURATION_FOR_PLAYERS = """
    SELECT
        id,
        key,
        min_players,
        max_players

    FROM board_configurations

    WHERE min_players <= ?
    AND max_players >= ?
"""


GET_ALL_CONFIGURATIONS = """
    SELECT
        id,
        key,
        min_players,
        max_players

    FROM board_configurations
"""

# =========================================================
# GET BOARDS BY GAME ID
# =========================================================

GET_BY_GAME_ID = """
    SELECT
        b.id,
        b.key,
        gb.position

    FROM game_boards gb

    JOIN boards b
        ON b.id = gb.board_id

    WHERE gb.game_id = ?

    ORDER BY gb.position
"""
