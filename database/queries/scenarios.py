from models.game import Scenario
from models.converters import row_to_scenario

def get_all(cursor) -> list[Scenario]:

    cursor.execute(
        """
        SELECT id, name, score_difficulty
        FROM scenarios
        ORDER BY name
        """
    )

    return [
        row_to_scenario(row)
        for row in cursor.fetchall()
    ]


def get_random(cursor) -> Scenario:

    cursor.execute(
        """
        SELECT id, name, score_difficulty
        FROM scenarios
        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    return row_to_scenario(
        cursor.fetchone()
    )


def get_by_name(cursor, name) -> Scenario:

    cursor.execute(
        """
        SELECT id, name, score_difficulty
        FROM scenarios
        WHERE name = ?
        """,
        (name,)
    )

    return row_to_scenario(
        cursor.fetchone()
    )

def get_by_id(cursor, game_id):
    
    cursor.execute(
        """
        SELECT
            s.id,
            s.name,
            s.score_difficulty

        FROM scenarios s

        JOIN game_scenarios gs
            ON gs.scenario_id = s.id

        WHERE gs.game_id = ?
        """,
        (game_id,)
    )

    return cursor.fetchall()

def get_scenario_difficulty(cursor, scenario_id):
    
    cursor.execute(
        """
        SELECT
            s.id,
            s.name,
            s.score_difficulty

        FROM scenarios s

        JOIN game_scenarios gs
            ON gs.scenario_id = s.id

        WHERE gs.game_id = ?
        """,
        (scenario_id,)
    )

    return row_to_scenario(
        cursor.fetchone()
    )