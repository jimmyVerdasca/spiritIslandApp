# =========================================================
# SAVE GAME
# =========================================================

SAVE_GAME = """
    INSERT INTO games (
        players,
        configuration_id,
        status
    )
    VALUES (?, ?, ?)
    RETURNING id
"""

SAVE_GAME_SPIRIT = """
    INSERT INTO game_spirits (
        game_id,
        spirit_id,
        position
    )
    VALUES (?, ?, ?)
"""

SAVE_GAME_BOARD = """
    INSERT INTO game_boards (
        game_id,
        board_id,
        position
    )
    VALUES (?, ?, ?)
"""


# =========================================================
# GET GAMES BY STATUS
# =========================================================

GET_BY_STATUS = """
    SELECT
        g.id,
        g.players,
        bc.key AS configuration,
        g.status,
        g.result,
        g.score,
        g.invader_cards_remaining,
        g.dahan_remaining,
        g.blight_remaining,
        g.created_at

    FROM games g

    JOIN board_configurations bc
        ON bc.id = g.configuration_id

    WHERE g.status = ?
      AND (? IS NULL OR g.result = ?)

    ORDER BY g.id DESC

    LIMIT ?
    OFFSET ?
"""

# =========================================================
# ABANDON GAME
# =========================================================

ABANDON_GAME = """
    UPDATE games

    SET
        status = ?,
        result = NULL

    WHERE id = ?
"""


# =========================================================
# FINISH GAME
# =========================================================

FINISH_GAME = """
    UPDATE games

    SET
        status = ?,
        result = ?,
        score = ?,
        invader_cards_remaining = ?,
        dahan_remaining = ?,
        blight_remaining = ?

    WHERE id = ?
"""