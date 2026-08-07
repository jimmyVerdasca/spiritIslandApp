def calculate_score(
    result,
    scenario_difficulty,
    adversary_difficulty,
    players,
    invader_cards,
    dahan,
    blight
):

    score = 0


    if result == "Victory":

        score += 5 * (scenario_difficulty + adversary_difficulty) + 1 # + 1 for the thematic map

        score += 10

        score += 2 * invader_cards


    else:

        score += 2 * (scenario_difficulty + adversary_difficulty) + 1

        score += invader_cards


    # group bonus/malus
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

    difficulty_score = (
        (scenario_difficulty + adversary_difficulty)
        * 5
    ) + 1

    victory_bonus = 10 if result == "Victory" else 0

    invader_bonus = invader_cards * 2

    survival_bonus = dahan // players
    blight_bonus = 0
    blight_bonus -= blight // players

    final_score = int(
        difficulty_score
        + victory_bonus
        + invader_bonus
        + survival_bonus
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