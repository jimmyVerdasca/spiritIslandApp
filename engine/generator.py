import random
from datetime import datetime
from database.database import database


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
    players=None,

    board=None,
    boards=None,

    adversaries=None,
    scenarios=None,

    adversary=None,
    difficulty=None,
    scenario=None,

    min_difficulty=None,
    max_difficulty=None
):

    with database() as db:

        cursor = db.cursor()
        # ----------------------------
        # Players
        # ----------------------------

        if players is None:
            players = random.randint(2,6)


        if players < 2 or players > 6:
            raise ValueError(
                "Players must be between 2 and 6"
            )


        minimum = min_difficulty or 1
        maximum = max_difficulty or 6


        if minimum > maximum:
            raise ValueError(
                "Invalid difficulty range"
            )


        # ----------------------------
        # Board
        # ----------------------------

        configuration = get_configuration(
            cursor,
            name=board,
            players=players
        )


        available_boards = get_available_boards(
            cursor,
            configuration["id"]
        )


        if len(available_boards) < players:
            raise Exception(
                "Not enough boards available for this configuration"
            )


        chosen_boards = random.sample(
            available_boards,
            players
        )


        if boards:

            # exact boards requested

            chosen_boards = boards

        else:

            chosen_boards = random.sample(
                available_boards,
                players
            )


        # ----------------------------
        # Spirits
        # ----------------------------

        chosen_spirits = get_random_spirits(
            cursor,
            players
        )


        # ----------------------------
        # Adversaries
        # ----------------------------

        chosen_adversaries = []


        all_adversaries = get_adversaries(cursor)


        if adversary:

            for name in adversary:

                chosen_adversaries.append(
                    {
                        "name": name,
                        "difficulty": random.randint(
                            minimum,
                            maximum
                        )
                    }
                )


        elif adversaries is not None:

            for adv in random.sample(
                all_adversaries,
                adversaries
            ):

                chosen_adversaries.append(
                    {
                        "name": adv["name"],
                        "difficulty": random.randint(
                            minimum,
                            maximum
                        )
                    }
                )
        else:

            if random.choice([True, False]):

                number = random.choice([1,2])

                for adv in random.sample(
                    all_adversaries,
                    number
                ):

                    chosen_adversaries.append(
                        {
                            "name": adv["name"],
                            "difficulty": random.randint(
                                minimum,
                                maximum
                            )
                        }
                    )


        # ----------------------------
        # Scenarios
        # ----------------------------

        chosen_scenarios = []


        all_scenarios = get_scenarios(cursor)


        if scenario:

            chosen_scenarios = scenario


        elif scenarios is not None:

            chosen_scenarios = [
                x["name"]
                for x in random.sample(
                    all_scenarios,
                    scenarios
                )
            ]
        else:

            if len(chosen_adversaries) < 2:

                number = random.choice(
                    [0,1,2]
                )

                if number:

                    chosen_scenarios = [
                        x["name"]
                        for x in random.sample(
                            all_scenarios,
                            number
                        )
                    ]


        # ----------------------------
        # Result
        # ----------------------------

        return {

            "players": players,

            "configuration": configuration["name"],

            "spirits": chosen_spirits,

            "boards": chosen_boards,

            "adversaries": chosen_adversaries,

            "scenarios": chosen_scenarios

        }