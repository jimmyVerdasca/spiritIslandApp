from models.game import (
    Game,
    Spirit,
    Board,
    Adversary,
    Scenario,
    GameAdversary,
    BoardConfiguration,
    Difficulty
)

from models.game_status import GameStatus


def row_to_spirit(row) -> Spirit:
    return Spirit(
        id=row["id"],
        name=row["name"]
    )


def row_to_board(row) -> Board:
    return Board(
        id=row["id"],
        name=row["name"]
    )


def row_to_adversary(row) -> Adversary:
    return Adversary(
        id=row["id"],
        name=row["name"]
    )

def row_to_difficulty(row) -> Difficulty:
    return Difficulty(
        id=row["id"],
        level=row["level"],
    )

def row_to_game_adversary(row) -> GameAdversary:
    
    return GameAdversary(
        adversary=Adversary(
            id=row["id"],
            name=row["name"]
        ),
        difficulty=Difficulty(
            id=row["id"],
            level=row["difficulty"]
        )
    )


def row_to_scenario(row) -> Scenario:
    return Scenario(
        id=row["id"],
        name=row["name"]
    )

def row_to_configuration(row) -> BoardConfiguration:
    
    return BoardConfiguration(
        id=row["id"],
        name=row["name"],
        min_players=row["min_players"],
        max_players=row["max_players"]
    )



def row_to_game(row) -> Game:
    return Game(
        id=row["id"],
        players=row["players"],
        configuration=row["configuration"],
        status=GameStatus(row["status"])
    )

def build_game(
    game_row,
    spirits,
    boards,
    adversaries,
    scenarios
) -> Game:

    game = row_to_game(game_row)

    game.spirits = spirits
    game.boards = boards
    game.adversaries = adversaries
    game.scenarios = scenarios

    return game