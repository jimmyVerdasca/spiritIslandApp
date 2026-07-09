def format_game(game):

    text = []

    print(game)

    text.append(
        f"Players: {game['players']}"
    )

    text.append(
        f"Board: {game['configuration']}"
    )

    text.append("")
    text.append("Spirits:")

    for spirit in game["spirits"]:
        text.append(
            f"- {spirit['name']}"
        )
        
    text.append("")
    text.append("Adversaries:")

    if game["adversaries"]:

        for adversary in game["adversaries"]:
            text.append(
                f"- {adversary['name']} (level {adversary['difficulty']})"
            )

    else:

        text.append(
            "- None"
        )


    text.append("")
    text.append("Scenarios:")

    if game["scenarios"]:

        for scenario in game["scenarios"]:
            if isinstance(scenario, dict):
                text.append(
                    f"- {scenario['name']}"
                )
            else:
                text.append(
                    f"- {scenario}"
                )

    else:

        text.append(
            "- None"
        )


    return "\n".join(text)