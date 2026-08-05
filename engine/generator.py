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
    get_available_boards
)

from database.queries.adversaries import (
    get_all as get_adversaries
)

from database.queries.scenarios import (
    get_all as get_scenarios
)



def generate_game(
    players: int | None = None,

    configuration: BoardConfiguration | None = None,
    spirits: list[Spirit | None] | None = None,
    boards: list[Board | None] | None = None,

    adversaries: list[Adversary] | None = None,
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

        available_boards = get_available_boards(
            cursor,
            configuration.id
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

        if adversary_count is None and adversaries is None:
            adversary_count = random.randint(0, 2)

        if scenario_count is None and scenarios is None:
            scenario_count = random.randint(
                0,
                2 - (adversary_count or 0)
            )


        # ----------------------------
        # Difficulty limits
        # ----------------------------

        minimum = min_difficulty or 1
        maximum = max_difficulty or 6

        if (scenario_count or 0) > 1:
            maximum = min(maximum, 4)

        if (adversary_count or 0) > 1:
            maximum -= adversary_count


        # ----------------------------
        # Adversaries
        # ----------------------------

        chosen_adversaries: list[GameAdversary] = []

        all_adversaries = get_adversaries(cursor)

        total_difficulty = 0

        if adversaries is None:

            adversaries = random.sample(
                all_adversaries,
                adversary_count
            )

        for adv in adversaries:

            upper = maximum - total_difficulty

            chosen_difficulty = random.randint(
                minimum,
                upper
            )

            total_difficulty += chosen_difficulty

            chosen_adversaries.append(
                GameAdversary(
                    adversary=adv,
                    difficulty=chosen_difficulty
                )
            )


        # ----------------------------
        # Scenarios
        # ----------------------------

        all_scenarios = get_scenarios(cursor)

        if scenarios is None:

            chosen_scenarios = random.sample(
                all_scenarios,
                scenario_count
            )

        else:

            chosen_scenarios = scenarios

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