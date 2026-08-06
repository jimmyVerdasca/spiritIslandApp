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

        score += 5 * (scenario_difficulty + adversary_difficulty + 1) # + 1 for the thematic map

        score += 10

        score += 2 * invader_cards


    else:

        score += 2 * (scenario_difficulty + adversary_difficulty + 1)

        score += invader_cards


    # group bonus/malus
    score += dahan // players

    score -= blight // players


    return score