from shared.models.game import Scenario
from shared.models.converters import row_to_scenario


def get_all(cursor) -> list[Scenario]:

    cursor.execute(
        """
        SELECT
            id,
            key,
            score_difficulty

        FROM scenarios

        ORDER BY key
        """
    )

    return [
        row_to_scenario(row)
        for row in cursor.fetchall()
    ]


def get_random(cursor) -> Scenario:

    cursor.execute(
        """
        SELECT
            id,
            key,
            score_difficulty

        FROM scenarios

        ORDER BY RANDOM()
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            "No scenarios found"
        )

    return row_to_scenario(row)


def get_by_key(cursor, key) -> Scenario:

    cursor.execute(
        """
        SELECT
            id,
            key,
            score_difficulty

        FROM scenarios

        WHERE key = ?
        """,
        (key,)
    )

    row = cursor.fetchone()

    if row is None:
        raise ValueError(
            f"Scenario not found: {key}"
        )

    return row_to_scenario(row)


def get_by_id(cursor, game_id) -> list[Scenario]:

    cursor.execute(
        """
        SELECT
            s.id,
            s.key,
            s.score_difficulty

        FROM scenarios s

        JOIN game_scenarios gs
            ON gs.scenario_id = s.id

        WHERE gs.game_id = ?
        """,
        (game_id,)
    )

    return [
        row_to_scenario(row)
        for row in cursor.fetchall()
    ]


def get_scenario_difficulty(
    cursor,
    scenario_id
) -> Scenario | None:

    cursor.execute(
        """
        SELECT
            id,
            key,
            score_difficulty

        FROM scenarios

        WHERE id = ?
        """,
        (scenario_id,)
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return row_to_scenario(row)