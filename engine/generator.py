import random
from datetime import datetime
from database.database import database, save_game
from models.game import *
from models.game_status import GameStatus


from database.queries.spirits import (
    get_all as get_spirits,
    get_random as get_random_spirits
)

from database.queries.boards import (
    get_configuration,
    get_all as get_boards
)

from database.queries.adversaries import (
    get_all as get_adversaries
)

from database.queries.scenarios import (
    get_all as get_scenarios
)

from database.queries.difficulties import (
    get_all as get_difficulties
)



def generate_game(
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

    with database() as db:

        cursor = db.cursor()
        # ----------------------------
        # Board configuration
        # ----------------------------

        if configuration is None:
            configuration = get_configuration(
                cursor,
                players=players
            )

        available_boards = get_boards(
            cursor
        )

        if players is None:
            players = random.randint(
                configuration.min_players,
                configuration.max_players
            )

        # ----------------------------
        # Boards
        # ----------------------------

        if boards is None:
    
            chosen_boards = random.sample(
                available_boards,
                players
            )

        else:

            chosen_boards = []

            selected_boards = [
                board
                for board in boards
                if board is not None
            ]


            chosen_boards.extend(
                selected_boards
            )


            missing = players - len(chosen_boards)


            if missing > 0:

                available = [
                    board
                    for board in available_boards
                    if board not in chosen_boards
                ]

                chosen_boards.extend(
                    random.sample(
                        available,
                        missing
                    )
                )


        # ----------------------------
        # Spirits
        # ----------------------------

        if spirits is None:

            # completely random
            chosen_spirits = get_random_spirits(
                cursor,
                players
            )

        else:

            all_spirits = get_spirits(cursor)

            chosen_spirits = []

            already_selected = [
                spirit
                for spirit in spirits
                if spirit is not None
            ]


            # keep selected spirits
            chosen_spirits.extend(
                already_selected
            )


            missing = players - len(chosen_spirits)


            if missing > 0:

                available = [
                    spirit
                    for spirit in all_spirits
                    if spirit not in chosen_spirits
                ]

                chosen_spirits.extend(
                    random.sample(
                        available,
                        missing
                    )
                )


        # ----------------------------
        # Random counts
        # ----------------------------

        user_selected_adversaries = (
            adversaries is not None
            and len(adversaries) > 0
        )

        user_selected_scenarios = (
            scenarios is not None
            and len(scenarios) > 0
        )


        # User did not define either
        if not user_selected_adversaries and not user_selected_scenarios:

            remaining = random.randint(0, 2)

            adversary_count = random.randint(
                0,
                remaining
            )

            scenario_count = remaining - adversary_count


        # User selected scenarios only
        elif not user_selected_adversaries and user_selected_scenarios:

            adversary_count = random.randint(
                0,
                max(0, 2 - len(scenarios))
            )


        # User selected adversaries only
        elif user_selected_adversaries and not user_selected_scenarios:

            scenario_count = random.randint(
                0,
                max(0, 2 - len(adversaries))
            )


        else:
            # User selected both
            adversary_count = len(adversaries)
            scenario_count = len(scenarios)


        # ----------------------------
        # Difficulty limits
        # ----------------------------

        minimum = min_difficulty or 1
        maximum = max_difficulty or 6

        if (scenario_count or 0) > 1:
            maximum = min(maximum, 4)


        # ----------------------------
        # Adversaries
        # ----------------------------

        chosen_adversaries = []

        all_adversaries = get_adversaries(cursor)
        all_difficulties = get_difficulties(cursor)

        available_adversaries = all_adversaries.copy()


        random_adversaries = (
            adversaries is None
            or len(adversaries) == 0
        )


        if random_adversaries:

            adversaries = [
                (None, None)
                for _ in range(adversary_count)
            ]


        respect_total_difficulty = len(adversaries) <= 6


        total_difficulty = 0


        for index, (adv, difficulty) in enumerate(adversaries):

            if adv is None:

                adv = random.choice(
                    available_adversaries
                )

                available_adversaries.remove(
                    adv
                )


            # User selected a difficulty -> keep it
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

                    # User choices may have made the remaining
                    # distribution impossible
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
                    # no balancing, just random difficulty
                    difficulty = random.choice(
                        all_difficulties
                    )


            total_difficulty += difficulty.level


            chosen_adversaries.append(
                GameAdversary(
                    adversary=adv,
                    difficulty=difficulty
                )
            )


        # ----------------------------
        # Scenarios
        # ----------------------------

        all_scenarios = get_scenarios(cursor)


        if scenarios is None:

            # No user input -> random amount
            chosen_scenarios = random.sample(
                all_scenarios,
                scenario_count
            )

        else:

            chosen_scenarios = []

            selected_scenarios = [
                s
                for s in scenarios
                if s is not None
            ]

            chosen_scenarios.extend(
                selected_scenarios
            )


            missing = len(scenarios) - len(chosen_scenarios)


            if missing > 0:

                available = [
                    s
                    for s in all_scenarios
                    if s not in chosen_scenarios
                ]

                chosen_scenarios.extend(
                    random.sample(
                        available,
                        missing
                    )
                )

        game = Game(
            players=players,
            configuration=configuration,
            spirits=chosen_spirits,
            boards=chosen_boards,
            adversaries=chosen_adversaries,
            scenarios=chosen_scenarios,
        )

        save_game(game)

        return game