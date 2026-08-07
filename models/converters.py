from models.game import (
    Game,
    Spirit,
    Board,
    Adversary,
    Scenario,
    GameAdversary,
    BoardConfiguration,
    Difficulty,
    AdversaryDifficulty
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
            id=row["adversary_id"],
            name=row["adversary_name"]
        ),
        difficulty=Difficulty(
            id=row["difficulty_id"],
            level=row["difficulty_level"]
        )
    )

def row_to_adversary_difficulty(row) -> AdversaryDifficulty:
    
    adversary = Adversary(
        id=row["adversary_id"],
        name=row["adversary_name"]
    )

    difficulty = Difficulty(
        id=row["difficulty_id"],
        level=row["difficulty_level"]
    )

    return AdversaryDifficulty(
        adversary=adversary,
        difficulty=difficulty,
        score_difficulty=row["score_difficulty"]
    )


def row_to_scenario(row) -> Scenario:
    return Scenario(
        id=row["id"],
        name=row["name"],
        score_difficulty=row["score_difficulty"]
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
        status=GameStatus(row["status"]),
        result=row["result"],
        score=row["score"],
        invader_cards_remaining=row["invader_cards_remaining"],
        dahan_remaining=row["dahan_remaining"],
        blight_remaining=row["blight_remaining"],
        created_at=row["created_at"],
    )

def row_to_adversary_difficulty(row):
    
    adversary = Adversary(
        id=row["adversary_id"],
        name=row["adversary_name"]
    )

    difficulty = Difficulty(
        id=row["difficulty_id"],
        level=row["difficulty_level"]
    )

    return AdversaryDifficulty(
        adversary=adversary,
        difficulty=difficulty,
        score_difficulty=row["score_difficulty"]
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