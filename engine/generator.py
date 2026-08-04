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
) -> Game:

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
            configuration.id
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
        # set quantity adversary & scenario to random pick
        # ----------------------------

        number_adversary = 0
        if not adversary:

            number_adversary = random.randint(0,2)

        number_scenario = 0
        if not scenario:
            number_scenario = random.randint(0,2 - number_adversary)

        
        # ----------------------------
        # set difficulty depending on number of adversary
        # ----------------------------

        if number_scenario > 1:
            maximum = 4 if (maximum > 4) else maximum

        if number_adversary > 1:
            maximum -= number_adversary

        # ----------------------------
        # Adversaries
        # ----------------------------

        chosen_adversaries = []

        all_adversaries = get_adversaries(cursor)

        total_difficulty = 0


        if adversary:

            # explicit adversary names provided
            for name in adversary:

                adversary_model = queries.adversaries.get_by_name(
                    cursor,
                    name
                )

                chosen_difficulty = random.randint(
                    minimum,
                    maximum - total_difficulty
                )

                total_difficulty += chosen_difficulty


                chosen_adversaries.append(
                    GameAdversary(
                        adversary=adversary_model,
                        difficulty=chosen_difficulty
                    )
                )


        elif adversaries is not None:

            for adv in random.sample(
                all_adversaries,
                adversaries
            ):

                chosen_difficulty = random.randint(
                    minimum,
                    maximum - total_difficulty
                )

                chosen_adversaries.append(
                    GameAdversary(
                        adversary=adv,
                        difficulty=chosen_difficulty
                    )
                )


        else:

            for adv in random.sample(
                all_adversaries,
                number_adversary
            ):

                chosen_difficulty = random.randint(
                    minimum,
                    maximum - total_difficulty
                )

                chosen_adversaries.append(
                    GameAdversary(
                        adversary=adv,
                        difficulty=chosen_difficulty
                    )
                )


        # ----------------------------
        # Scenarios
        # ----------------------------

        chosen_scenarios = []

        all_scenarios = get_scenarios(cursor)


        if scenario:

            # explicit scenario names provided
            chosen_scenarios = [
                queries.scenarios.get_by_name(
                    cursor,
                    name
                )
                for name in scenario
            ]


        elif scenarios is not None:

            chosen_scenarios = random.sample(
                all_scenarios,
                scenarios
            )


        else:

            chosen_scenarios = random.sample(
                all_scenarios,
                number_scenario
    )


        # ----------------------------
        # Result
        # ----------------------------

        gameObject = Game(

            players=players,

            configuration=configuration.name,

            spirits=chosen_spirits,

            boards=chosen_boards,

            adversaries=chosen_adversaries,

            scenarios=chosen_scenarios
        )

        save_game(gameObject)

        return gameObject