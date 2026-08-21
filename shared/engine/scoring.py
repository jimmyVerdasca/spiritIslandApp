
def calculate_score(
    result,
    scenario_difficulty,
    adversary_difficulty,
    players,
    invader_cards,
    dahan,
    blight
):

    if result == "Victory":

        score = (
            5 * (scenario_difficulty + adversary_difficulty)
            + 1
            + 10
            + 2 * invader_cards
        )

    else:

        score = (
            2 * (scenario_difficulty + adversary_difficulty)
            + 1
            + invader_cards
        )


    # Group bonus / malus

    score += dahan // players
    score -= blight // players


    return score


def calculate_score_breakdown(
    result,
    scenario_difficulty,
    adversary_difficulty,
    players,
    invader_cards,
    dahan,
    blight
):

    if result == "Victory":

        difficulty_score = (
            5 * (scenario_difficulty + adversary_difficulty)
            + 1
        )

        victory_bonus = 10
        invader_bonus = invader_cards * 2

    else:

        difficulty_score = (
            2 * (scenario_difficulty + adversary_difficulty)
            + 1
        )

        victory_bonus = 0
        invader_bonus = invader_cards


    survival_bonus = dahan // players
    blight_bonus = -(blight // players)


    final_score = int(
        difficulty_score
        + victory_bonus
        + invader_bonus
        + survival_bonus
        + blight_bonus
    )


    return {
        "difficulty": difficulty_score,
        "difficulty_detail": (
            scenario_difficulty,
            adversary_difficulty
        ),
        "victory_bonus": victory_bonus,
        "invader_bonus": invader_bonus,
        "survival_bonus": survival_bonus,
        "blight_bonus": blight_bonus,
        "final": final_score,
    }

def calculate_game_difficulty(game):
    """
    Calculate the total difficulty contribution of all
    adversaries and scenarios in a completed game.

    Returns:
        tuple:
            (
                adversary_difficulty,
                scenario_difficulty,
            )
    """


    adversary_difficulty = sum(
        game_adversary.score_difficulty
        for game_adversary in game.adversaries
    )

    scenario_difficulty = sum(
        scenario.score_difficulty
        for scenario in game.scenarios
    )

    return (
        adversary_difficulty,
        scenario_difficulty,
    )