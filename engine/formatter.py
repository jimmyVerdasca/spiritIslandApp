from models.game import Game


def format_game(game: Game) -> str:

    text = []

    print(game)

    text.append(
        f"Players: {game.players}"
    )

    text.append(
        f"Board: {game.configuration.name}"
    )

    text.append("")
    text.append("Spirits:")

    for spirit, board in zip(game.spirits, game.boards):
        text.append(
            f"- {spirit.name} ({board.name})"
        )


    text.append("")
    text.append("Adversaries:")

    if game.adversaries:
    
        for game_adversary in game.adversaries:

            difficulty = (
                f"level {game_adversary.difficulty.level}"
                if game_adversary.difficulty is not None
                else "any level"
            )

            text.append(
                f"- {game_adversary.adversary.name} "
                f"({difficulty})"
            )

    else:

        text.append(
            "- None"
        )


    text.append("")
    text.append("Scenarios:")

    if game.scenarios:

        for scenario in game.scenarios:
            text.append(
                f"- {scenario.name}"
            )

    else:

        text.append(
            "- None"
        )


    return "\n".join(text)