from shared.models.game import Game
from shared.models.game_status import GameStatus
from shared.models.converters import row_to_game


# =========================================================
# SAVE GAME
# =========================================================

def save_game(cursor, game: Game) -> int:

    configuration = game.configuration

    cursor.execute(
        """
        INSERT INTO games(
            players,
            configuration_id,
            status
        )
        VALUES (?, ?, ?)
        """,
        (
            game.players,
            configuration.id,
            game.status.value
        )
    )

    game_id = cursor.lastrowid


    # =====================================================
    # SPIRITS
    # =====================================================

    for position, spirit in enumerate(
        game.spirits,
        start=1
    ):

        cursor.execute(
            """
            INSERT INTO game_spirits
            (
                game_id,
                spirit_id,
                position
            )
            VALUES (?, ?, ?)
            """,
            (
                game_id,
                spirit.id,
                position
            )
        )


    # =====================================================
    # BOARDS
    # =====================================================

    for position, board in enumerate(
        game.boards,
        start=1
    ):

        cursor.execute(
            """
            INSERT INTO game_boards
            (
                game_id,
                board_id,
                position
            )
            VALUES (?, ?, ?)
            """,
            (
                game_id,
                board.id,
                position
            )
        )


    # =====================================================
    # ADVERSARIES
    # =====================================================

    for game_adversary in game.adversaries:

        adversary = game_adversary.adversary
        difficulty = game_adversary.difficulty

        cursor.execute(
            """
            INSERT INTO game_adversaries
            (
                game_id,
                adversary_id,
                difficulty_id
            )
            VALUES (?, ?, ?)
            """,
            (
                game_id,
                adversary.id,
                difficulty.id,
            )
        )


    # =====================================================
    # SCENARIOS
    # =====================================================

    for scenario in game.scenarios:

        cursor.execute(
            """
            INSERT INTO game_scenarios
            (
                game_id,
                scenario_id
            )
            VALUES (?, ?)
            """,
            (
                game_id,
                scenario.id
            )
        )


    return game_id


# =========================================================
# GET GAMES BY STATUS
# =========================================================

def get_by_status(
    cursor,
    status,
    result=None,
    limit=20,
    offset=0,
):

    query = """
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
    """

    params = [status.value]

    if result is not None:

        query += """
            AND g.result = ?
        """

        params.append(result)

    query += """
        ORDER BY g.id DESC
        LIMIT ?
        OFFSET ?
    """

    params.extend([
        limit,
        offset,
    ])

    cursor.execute(
        query,
        params
    )

    return cursor.fetchall()


# =========================================================
# ABANDON GAME
# =========================================================

def abandon_game(
    cursor,
    game_id
):

    cursor.execute(
        """
        UPDATE games

        SET
            status = ?,
            result = NULL

        WHERE id = ?
        """,
        (
            GameStatus.ABANDONED.value,
            game_id
        )
    )


# =========================================================
# FINISH GAME
# =========================================================

def finish_game(
    cursor,
    game_id,
    result,
    score,
    invader_cards,
    dahan,
    blight
):

    cursor.execute(
        """
        UPDATE games

        SET
            status = ?,
            result = ?,
            score = ?,
            invader_cards_remaining = ?,
            dahan_remaining = ?,
            blight_remaining = ?

        WHERE id = ?
        """,
        (
            GameStatus.FINISHED.value,
            result,
            score,
            invader_cards,
            dahan,
            blight,
            game_id
        )
    )