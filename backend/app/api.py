from fastapi import APIRouter

from shared.data_access.factory import create_data_provider
from shared.models.converters import (
    game_to_json,
    spirit_to_json,
    board_to_json,
    configuration_to_json,
    adversary_to_json,
    difficulty_to_json,
    scenario_to_json,
    adversary_difficulty_to_json,
    trophy_to_json,
    json_to_game,
)


router = APIRouter()


data = create_data_provider(
    application="backend",
)


# =========================================================
# Static data
# =========================================================

@router.get("/configurations")
def get_configurations():

    return [
        configuration_to_json(item)
        for item in data.configurations
    ]


@router.get("/spirits")
def get_spirits():

    return [
        spirit_to_json(item)
        for item in data.spirits
    ]


@router.get("/boards")
def get_boards():

    return [
        board_to_json(item)
        for item in data.boards
    ]


@router.get("/adversaries")
def get_adversaries():

    return [
        adversary_to_json(item)
        for item in data.adversaries
    ]


@router.get("/difficulties")
def get_difficulties():

    return [
        difficulty_to_json(item)
        for item in data.difficulties
    ]


@router.get("/scenarios")
def get_scenarios():

    return [
        scenario_to_json(item)
        for item in data.scenarios
    ]


@router.get("/adversaries-difficulties")
def get_adversaries_difficulties():

    return [
        adversary_difficulty_to_json(item)
        for item in data.adversaries_difficulties
    ]


@router.get("/trophies")
def get_trophies():

    return [
        trophy_to_json(item)
        for item in data.trophies
    ]


# =========================================================
# Games
# =========================================================

@router.post("/games")
def save_game(game: dict):

    game_object = json_to_game(game)

    game_id = data.save_game(
        game_object
    )

    return {
        "id": game_id
    }


@router.get("/games/running")
def get_running_games(
    limit: int = 20,
    offset: int = 0,
):

    games = data.get_running_games(
        limit=limit,
        offset=offset,
    )

    return [
        game_to_json(game)
        for game in games
    ]


@router.get("/games/finished")
def get_finished_games(
    result: str | None = None,
    limit: int = 20,
    offset: int = 0,
):

    games = data.get_finished_games(
        result=result,
        limit=limit,
        offset=offset,
    )

    return [
        game_to_json(game)
        for game in games
    ]


@router.get("/games/abandoned")
def get_abandoned_games(
    limit: int = 20,
    offset: int = 0,
):

    games = data.get_abandoned_games(
        limit=limit,
        offset=offset,
    )

    return [
        game_to_json(game)
        for game in games
    ]


# =========================================================
# Game state
# =========================================================

@router.post("/games/{game_id}/abandon")
def abandon_game(
    game_id: int,
):

    data.abandon_game(
        game_id
    )

    return None


@router.post("/games/{game_id}/finish")
def finish_game(
    game_id: int,
    payload: dict,
):

    data.finish_game(
        game_id=game_id,
        result=payload["result"],
        score=payload["score"],
        invader_cards=payload["invader_cards"],
        dahan=payload["dahan"],
        blight=payload["blight"],
    )

    return None