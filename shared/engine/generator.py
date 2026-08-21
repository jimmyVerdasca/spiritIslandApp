import random
from shared.models.game import *



def generate_game(
    data,
    players: int | None = None,

    configuration: BoardConfiguration | None = None,
    spirits: list[Spirit | None] | None = None,
    boards: list[Board | None] | None = None,

    adversaries: list[tuple[Adversary, Difficulty]] | None = None,
    adversary_count: int | None = None,

    scenarios: list[Scenario] | None = None,
    scenario_count: int | None = None,

    difficulty: int | None = None,
    min_difficulty: int | None = None,
    max_difficulty: int | None = None,
) -> Game:

    print(players)
    print(configuration)
 # ====================================================
    # Board configuration
    # ====================================================

    if configuration is None:

        if players is not None:

            configurations = [
                configuration
                for configuration in data.configurations
                if (
                    configuration.min_players
                    <= players
                    <= configuration.max_players
                )
            ]

            if configurations:

                configuration = random.choice(
                    configurations
                )

        else:

            configuration = random.choice(
                data.configurations
            )


    # ====================================================
    # Players
    # ====================================================

    if players is None:

        players = random.randint(
            configuration.min_players,
            configuration.max_players,
        )


    # ====================================================
    # Boards
    # ====================================================

    available_boards = list(
        data.boards
    )


    if boards is None:

        chosen_boards = random.sample(
            available_boards,
            players,
        )

    else:

        # Preserve player positions
        chosen_boards = list(
            boards
        )


        # Boards already explicitly selected
        selected_boards = [
            board
            for board in chosen_boards
            if board is not None
        ]


        available = [
            board
            for board in available_boards
            if board not in selected_boards
        ]


        # Fill only the "Any" positions
        for index, board in enumerate(
            chosen_boards
        ):

            if board is None:

                chosen_boards[index] = (
                    random.choice(
                        available
                    )
                )

                available.remove(
                    chosen_boards[index]
                )


    # ====================================================
    # Spirits
    # ====================================================

    available_spirits = list(
        data.spirits
    )


    if spirits is None:

        chosen_spirits = random.sample(
            available_spirits,
            players,
        )

    else:

        # Preserve player positions
        chosen_spirits = list(
            spirits
        )


        # Spirits already explicitly selected
        selected_spirits = [
            spirit
            for spirit in chosen_spirits
            if spirit is not None
        ]


        available = [
            spirit
            for spirit in available_spirits
            if spirit not in selected_spirits
        ]


        # Fill only the "Any" positions
        for index, spirit in enumerate(
            chosen_spirits
        ):

            if spirit is None:

                chosen_spirits[index] = (
                    random.choice(
                        available
                    )
                )

                available.remove(
                    chosen_spirits[index]
                )


    # ====================================================
    # Random counts
    # ====================================================

    user_selected_adversaries = (
        adversaries is not None
        and len(adversaries) > 0
    )

    user_selected_scenarios = (
        scenarios is not None
        and len(scenarios) > 0
    )


    # ----------------------------------------------------
    # User selected neither
    # ----------------------------------------------------

    if (
        not user_selected_adversaries
        and not user_selected_scenarios
    ):

        remaining = random.randint(
            0,
            2,
        )

        adversary_count = random.randint(
            0,
            remaining,
        )

        scenario_count = (
            remaining
            - adversary_count
        )


    # ----------------------------------------------------
    # User selected scenarios only
    # ----------------------------------------------------

    elif (
        not user_selected_adversaries
        and user_selected_scenarios
    ):

        adversary_count = random.randint(
            0,
            max(
                0,
                2 - len(scenarios),
            ),
        )


    # ----------------------------------------------------
    # User selected adversaries only
    # ----------------------------------------------------

    elif (
        user_selected_adversaries
        and not user_selected_scenarios
    ):

        scenario_count = random.randint(
            0,
            max(
                0,
                2 - len(adversaries),
            ),
        )


    # ----------------------------------------------------
    # User selected both
    # ----------------------------------------------------

    else:

        adversary_count = len(
            adversaries
        )

        scenario_count = len(
            scenarios
        )


    # ====================================================
    # Difficulty limits
    # ====================================================

    minimum = (
        min_difficulty
        if min_difficulty is not None
        else 1
    )

    maximum = (
        max_difficulty
        if max_difficulty is not None
        else 6
    )


    # More than one scenario limits total difficulty
    if (scenario_count or 0) > 1:

        maximum = min(
            maximum,
            4,
        )


    # ====================================================
    # Adversaries
    # ====================================================

    chosen_adversaries = []


    all_adversaries = list(
        data.adversaries
    )

    all_difficulties = list(
        data.difficulties
    )


    available_adversaries = (
        all_adversaries.copy()
    )


    random_adversaries = (
        adversaries is None
        or len(adversaries) == 0
    )


    if random_adversaries:

        adversaries = [
            (None, None)
            for _ in range(
                adversary_count
            )
        ]


    respect_total_difficulty = (
        len(adversaries) <= 6
    )


    total_difficulty = 0


    for index, (
        adversary,
        selected_difficulty,
    ) in enumerate(adversaries):

        # ------------------------------------------------
        # Select adversary
        # ------------------------------------------------

        if adversary is None:

            adversary = random.choice(
                available_adversaries
            )

            available_adversaries.remove(
                adversary
            )


        # ------------------------------------------------
        # Select difficulty
        # ------------------------------------------------

        difficulty = selected_difficulty


        if difficulty is None:

            if respect_total_difficulty:

                remaining_points = (
                    maximum
                    - total_difficulty
                )


                remaining_adversaries = (
                    len(adversaries)
                    - index
                    - 1
                )


                max_for_this_adversary = (
                    remaining_points
                    - remaining_adversaries
                )


                possible_difficulties = [
                    d
                    for d in all_difficulties
                    if (
                        minimum
                        <= d.level
                        <= max_for_this_adversary
                    )
                ]


                if possible_difficulties:

                    difficulty = random.choice(
                        possible_difficulties
                    )

                else:

                    difficulty = random.choice(
                        all_difficulties
                    )

            else:

                # More than 6 adversaries:
                # no total-difficulty balancing.
                difficulty = random.choice(
                    all_difficulties
                )


        # ------------------------------------------------
        # Track difficulty
        # ------------------------------------------------

        total_difficulty += (
            difficulty.level
        )


        # ------------------------------------------------
        # Create GameAdversary
        # ------------------------------------------------

        try:

            score_difficulty = data.adversaries_difficulties[
                (
                    adversary.id,
                    difficulty.id,
                )
            ]

        except KeyError:

            raise RuntimeError(
                "Invalid adversary/difficulty combination: "
                f"({adversary.id}, {difficulty.id})"
            )


        chosen_adversaries.append(
            GameAdversary(
                adversary=adversary,
                difficulty=difficulty,
                score_difficulty=score_difficulty,
            )
        )


    # ====================================================
    # Scenarios
    # ====================================================

    all_scenarios = list(
        data.scenarios
    )


    if scenarios is None:

        chosen_scenarios = random.sample(
            all_scenarios,
            scenario_count,
        )

    else:

        chosen_scenarios = [
            scenario
            for scenario in scenarios
            if scenario is not None
        ]


        missing = (
            len(scenarios)
            - len(chosen_scenarios)
        )


        if missing > 0:

            available = [
                scenario
                for scenario in all_scenarios
                if scenario not in chosen_scenarios
            ]


            chosen_scenarios.extend(
                random.sample(
                    available,
                    missing,
                )
            )


    # ====================================================
    # Create game
    # ====================================================

    return Game(
        players=players,
        configuration=configuration,
        spirits=chosen_spirits,
        boards=chosen_boards,
        adversaries=chosen_adversaries,
        scenarios=chosen_scenarios,
    )
