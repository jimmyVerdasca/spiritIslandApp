from models.game import (
    Game,
    Spirit,
    Board,
    Adversary,
    Scenario,
    GameAdversary,
    BoardConfiguration,
    Difficulty,
    AdversaryDifficulty,
    Trophy,
)

from models.game_status import GameStatus


# =========================================================
# SQL row converters
# =========================================================

def row_to_spirit(row) -> Spirit:

    return Spirit(
        id=row["id"],
        key=row["key"],
    )


def row_to_board(row) -> Board:

    return Board(
        id=row["id"],
        key=row["key"],
    )


def row_to_adversary(row) -> Adversary:

    return Adversary(
        id=row["id"],
        key=row["key"],
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
            key=row["adversary_key"],
        ),

        difficulty=Difficulty(
            id=row["difficulty_id"],
            level=row["difficulty_level"],
        ),
        score_difficulty=row["score_difficulty"],
    )


def row_to_adversary_difficulty(row) -> AdversaryDifficulty:

    adversary = Adversary(
        id=row["adversary_id"],
        key=row["adversary_key"],
    )

    difficulty = Difficulty(
        id=row["difficulty_id"],
        level=row["difficulty_level"],
    )

    return AdversaryDifficulty(
        adversary=adversary,
        difficulty=difficulty,
        score_difficulty=row["score_difficulty"],
    )


def row_to_scenario(row) -> Scenario:

    return Scenario(
        id=row["id"],
        key=row["key"],
        score_difficulty=row["score_difficulty"],
    )


def row_to_configuration(row) -> BoardConfiguration:

    return BoardConfiguration(
        id=row["id"],
        key=row["key"],
        min_players=row["min_players"],
        max_players=row["max_players"],
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


def build_game(
    game_row,
    spirits,
    boards,
    adversaries,
    scenarios,
) -> Game:

    game = row_to_game(
        game_row
    )

    game.spirits = spirits
    game.boards = boards
    game.adversaries = adversaries
    game.scenarios = scenarios

    return game


def row_to_trophy(row) -> Trophy:

    return Trophy(
        id=row["id"],
        key=row["key"],
        locked_image=row["locked_image"],
        unlocked_image=row["unlocked_image"],
        sql_condition=row["sql_condition"],
        python_condition=row["python_condition"],
    )




# =========================================================
# JSON converters
# =========================================================

def json_to_spirit(data) -> Spirit:

    return Spirit(
        id=data["id"],
        key=data["key"],
    )


def spirit_to_json(spirit: Spirit) -> dict:

    return {
        "id": spirit.id,
        "key": spirit.key,
    }


def json_to_board(data) -> Board:

    return Board(
        id=data["id"],
        key=data["key"],
    )


def board_to_json(board: Board) -> dict:

    return {
        "id": board.id,
        "key": board.key,
    }


def json_to_configuration(
    data,
) -> BoardConfiguration:

    return BoardConfiguration(
        id=data["id"],
        key=data["key"],
        min_players=data["min_players"],
        max_players=data["max_players"],
    )


def configuration_to_json(
    configuration: BoardConfiguration,
) -> dict:

    return {
        "id": configuration.id,
        "key": configuration.key,
        "min_players": configuration.min_players,
        "max_players": configuration.max_players,
    }


def json_to_adversary(data) -> Adversary:

    return Adversary(
        id=data["id"],
        key=data["key"],
    )


def adversary_to_json(
    adversary: Adversary,
) -> dict:

    return {
        "id": adversary.id,
        "key": adversary.key,
    }


def json_to_difficulty(data) -> Difficulty:

    return Difficulty(
        id=data["id"],
        level=data["level"],
    )


def difficulty_to_json(
    difficulty: Difficulty,
) -> dict:

    return {
        "id": difficulty.id,
        "level": difficulty.level,
    }


def json_to_game_adversary(
    data,
) -> GameAdversary:

    return GameAdversary(
        adversary=json_to_adversary(
            data["adversary"]
        ),
        difficulty=json_to_difficulty(
            data["difficulty"]
        ),
        score_difficulty=data["score_difficulty"],
    )


def game_adversary_to_json(
    adversary: GameAdversary,
) -> dict:

    return {
        "adversary": adversary_to_json(
            adversary.adversary
        ),
        "difficulty": difficulty_to_json(
            adversary.difficulty
        ),
        "score_difficulty": (
            adversary.score_difficulty
        ),
    }


def json_to_adversary_difficulty(
    data,
) -> AdversaryDifficulty:

    return AdversaryDifficulty(
        adversary=json_to_adversary(
            data["adversary"]
        ),
        difficulty=json_to_difficulty(
            data["difficulty"]
        ),
        score_difficulty=data["score_difficulty"],
    )


def adversary_difficulty_to_json(
    combination: AdversaryDifficulty,
) -> dict:

    return {
        "adversary": adversary_to_json(
            combination.adversary
        ),
        "difficulty": difficulty_to_json(
            combination.difficulty
        ),
        "score_difficulty": (
            combination.score_difficulty
        ),
    }


def json_to_scenario(data) -> Scenario:

    return Scenario(
        id=data["id"],
        key=data["key"],
        score_difficulty=data["score_difficulty"],
    )


def scenario_to_json(
    scenario: Scenario,
) -> dict:

    return {
        "id": scenario.id,
        "key": scenario.key,
        "score_difficulty": (
            scenario.score_difficulty
        ),
    }


def json_to_game(data) -> Game:

    return Game(
        id=data.get("id"),
        players=data.get("players", 0),

        configuration=(
            json_to_configuration(
                data["configuration"]
            )
            if data.get("configuration") is not None
            else None
        ),

        spirits=[
            json_to_spirit(item)
            for item in data.get("spirits", [])
        ],

        boards=[
            json_to_board(item)
            for item in data.get("boards", [])
        ],

        adversaries=[
            json_to_game_adversary(item)
            for item in data.get("adversaries", [])
        ],

        scenarios=[
            json_to_scenario(item)
            for item in data.get("scenarios", [])
        ],

        status=GameStatus(
            data.get(
                "status",
                GameStatus.RUNNING.value,
            )
        ),

        result=data.get("result"),
        score=data.get("score"),

        invader_cards_remaining=(
            data.get("invader_cards_remaining")
        ),

        dahan_remaining=(
            data.get("dahan_remaining")
        ),

        blight_remaining=(
            data.get("blight_remaining")
        ),

        created_at=data.get("created_at"),
    )


def game_to_json(game: Game) -> dict:

    return {
        "id": game.id,
        "players": game.players,

        "configuration": (
            configuration_to_json(
                game.configuration
            )
            if game.configuration is not None
            else None
        ),

        "spirits": [
            spirit_to_json(spirit)
            for spirit in game.spirits
        ],

        "boards": [
            board_to_json(board)
            for board in game.boards
        ],

        "adversaries": [
            game_adversary_to_json(adversary)
            for adversary in game.adversaries
        ],

        "scenarios": [
            scenario_to_json(scenario)
            for scenario in game.scenarios
        ],

        "status": game.status.value,

        "result": game.result,
        "score": game.score,

        "invader_cards_remaining": (
            game.invader_cards_remaining
        ),

        "dahan_remaining": (
            game.dahan_remaining
        ),

        "blight_remaining": (
            game.blight_remaining
        ),

        "created_at": game.created_at,
    }


def json_to_trophy(data) -> Trophy:

    return Trophy(
        id=data["id"],
        key=data["key"],
        locked_image=data["locked_image"],
        unlocked_image=data["unlocked_image"],
        sql_condition=data["sql_condition"],
        python_condition=data["python_condition"],
        unlocked=data.get("unlocked", False),
    )


def trophy_to_json(trophy: Trophy) -> dict:

    return {
        "id": trophy.id,
        "key": trophy.key,
        "locked_image": trophy.locked_image,
        "unlocked_image": trophy.unlocked_image,
        "sql_condition": trophy.sql_condition,
        "python_condition": trophy.python_condition,
        "unlocked": trophy.unlocked,
    }