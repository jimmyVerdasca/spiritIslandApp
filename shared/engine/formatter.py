from kivy.app import App

from shared.models.game import Game


def format_game(game: Game) -> str:

    app = App.get_running_app()

    if app is None:
        raise RuntimeError(
            "Kivy application is not running"
        )

    language = app.language_manager

    text = []

    # =========================================================
    # Players
    # =========================================================

    players_label = language.get(
        "players"
    )

    text.append(
        f"{players_label}: {game.players}"
    )

    # =========================================================
    # Board
    # =========================================================

    board_label = language.get(
        "board"
    )

    board_name = language.get(
        game.configuration.key,
        "board_configurations"
    )

    text.append(
        f"{board_label}: {board_name}"
    )

    # =========================================================
    # Spirits
    # =========================================================

    spirits_title = language.get(
        "spirits_title"
    )

    text.append("")
    text.append(
        f"{spirits_title}:"
    )

    for spirit, board in zip(
        game.spirits,
        game.boards
    ):

        spirit_name = language.get(
            spirit.key,
            "spirits"
        )

        board_name = language.get(
            board.key,
            "boards"
        )

        text.append(
            f"- {spirit_name} ({board_name})"
        )

    # =========================================================
    # Adversaries
    # =========================================================

    adversaries_title = language.get(
        "adversaries_title"
    )

    level_label = language.get(
        "level"
    )

    any_level_text = language.get(
        "any_level"
    )

    none_text = language.get(
        "none"
    )

    text.append("")
    text.append(
        f"{adversaries_title}:"
    )

    if game.adversaries:

        for game_adversary in game.adversaries:

            adversary_name = language.get(
                game_adversary.adversary.key,
                "adversaries"
            )

            if game_adversary.difficulty is not None:

                difficulty = (
                    f"{level_label} "
                    f"{game_adversary.difficulty.level}"
                )

            else:

                difficulty = any_level_text

            text.append(
                f"- {adversary_name} ({difficulty})"
            )

    else:

        text.append(
            f"- {none_text}"
        )

    # =========================================================
    # Scenarios
    # =========================================================

    scenarios_title = language.get(
        "scenarios_title"
    )

    text.append("")
    text.append(
        f"{scenarios_title}:"
    )

    if game.scenarios:

        for scenario in game.scenarios:

            scenario_name = language.get(
                scenario.key,
                "scenarios"
            )

            text.append(
                f"- {scenario_name}"
            )

    else:

        text.append(
            f"- {none_text}"
        )

    return "\n".join(text)