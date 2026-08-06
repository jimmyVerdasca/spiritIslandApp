from .. import queries
from models.game import Game
from models.game_status import GameStatus


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


    # ----------------------------
    # Spirits
    # ----------------------------

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


    # ----------------------------
    # Boards
    # ----------------------------

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


    # ----------------------------
    # Adversaries
    # ----------------------------

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


    # ----------------------------
    # Scenarios
    # ----------------------------

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



def finish_game(cursor, game_id: int):

    cursor.execute(
        """
        UPDATE games

        SET
            status = ?,
            finished_at = CURRENT_TIMESTAMP

        WHERE id = ?
        """,
        (
            GameStatus.FINISHED.value,
            game_id
        )
    )



def get_by_status(cursor, status: GameStatus, limit, offset):

    cursor.execute(
        """
        SELECT
            g.id,
            g.players,
            g.status,
            g.created_at,

            bc.name AS configuration

        FROM games g

        JOIN board_configurations bc
            ON bc.id = g.configuration_id

        WHERE g.status = ?

        ORDER BY g.created_at DESC

        LIMIT ?
        OFFSET ?
        """,
        (
            status.value,
            limit,
            offset
        )
    )

    return cursor.fetchall()

def abandon_game(cursor, game_id):

    cursor.execute(
        """
        UPDATE games
        SET status = ?
        WHERE id = ?
        AND status = ?
        """,
        (
            GameStatus.ABANDONED.value,
            game_id,
            GameStatus.RUNNING.value
        )
    )