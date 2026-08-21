def seed_trophies(cursor):
    cursor.executemany(
        """
        INSERT INTO trophies (
            key,
            locked_image,
            unlocked_image,
            sql_condition,
            python_condition
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        TROPHIES,
    )


TROPHIES = [

    # =========================================================
    # First games
    # =========================================================

    (
        "first_steps",
        "trophy_locked.png",
        "first_steps.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE status = 'FINISHED'
        )
        """,
        None,
    ),

    (
        "first_victory",
        "trophy_locked.png",
        "first_victory.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE result = 'Victory'
        )
        """,
        None,
    ),


    # =========================================================
    # Difficulty
    # =========================================================

    *[
        (
            f"difficulty_{i}",
            "difficulty_locked.png",
            f"difficulty_{i}.png",
            f"""
            SELECT EXISTS(
                SELECT 1
                FROM games g
                WHERE
                    g.result = 'Victory'
                    AND g.score IS NOT NULL
                    AND (
                        SELECT
                            COALESCE(SUM(d.level), 0)
                        FROM game_adversaries ga
                        JOIN difficulties d
                            ON d.id = ga.difficulty_id
                        WHERE ga.game_id = g.id
                    )
                    +
                    (
                        SELECT
                            COALESCE(SUM(s.score_difficulty), 0)
                        FROM game_scenarios gs
                        JOIN scenarios s
                            ON s.id = gs.scenario_id
                        WHERE gs.game_id = g.id
                    )
                    >= {i}
            )
            """,
            None,
        )
        for i in range(1, 10)
    ],


    # =========================================================
    # Adversaries
    # =========================================================

    (
        "level_6_challenger",
        "level6_locked.png",
        "level6.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games g
            JOIN game_adversaries ga
                ON ga.game_id = g.id
            JOIN difficulties d
                ON d.id = ga.difficulty_id
            WHERE
                g.result = 'Victory'
                AND d.level = 6
        )
        """,
        None,
    ),

    (
        "adversary_master",
        "adversary_master_locked.png",
        "adversary_master.png",
        """
        SELECT NOT EXISTS(
            SELECT 1
            FROM adversaries a
            WHERE NOT EXISTS(
                SELECT 1
                FROM games g
                JOIN game_adversaries ga
                    ON ga.game_id = g.id
                WHERE
                    g.result = 'Victory'
                    AND ga.adversary_id = a.id
            )
        )
        """,
        None,
    ),

    (
        "level_6_master",
        "level6_master_locked.png",
        "level6_master.png",
        """
        SELECT NOT EXISTS(
            SELECT 1
            FROM adversaries a
            WHERE NOT EXISTS(
                SELECT 1
                FROM games g
                JOIN game_adversaries ga
                    ON ga.game_id = g.id
                JOIN difficulties d
                    ON d.id = ga.difficulty_id
                WHERE
                    g.result = 'Victory'
                    AND ga.adversary_id = a.id
                    AND d.level = 6
            )
        )
        """,
        None,
    ),

    (
        "double_trouble",
        "double_locked.png",
        "double.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games g
            JOIN game_adversaries ga
                ON ga.game_id = g.id
            WHERE g.result = 'Victory'
            GROUP BY g.id
            HAVING COUNT(*) >= 2
        )
        """,
        None,
    ),


    # =========================================================
    # Spirits
    # =========================================================

    (
        "spirit_explorer",
        "spirit_locked.png",
        "spirit_explorer.png",
        """
        SELECT NOT EXISTS(
            SELECT 1
            FROM spirits s
            WHERE NOT EXISTS(
                SELECT 1
                FROM games g
                JOIN game_spirits gs
                    ON gs.game_id = g.id
                WHERE
                    g.result = 'Victory'
                    AND gs.spirit_id = s.id
            )
        )
        """,
        None,
    ),


    # =========================================================
    # Scenarios
    # =========================================================

    (
        "scenario_explorer",
        "scenario_locked.png",
        "scenario_explorer.png",
        """
        SELECT NOT EXISTS(
            SELECT 1
            FROM scenarios s
            WHERE NOT EXISTS(
                SELECT 1
                FROM games g
                JOIN game_scenarios gs
                    ON gs.game_id = g.id
                WHERE
                    g.result = 'Victory'
                    AND gs.scenario_id = s.id
            )
        )
        """,
        None,
    ),


    # =========================================================
    # Players
    # =========================================================

    (
        "true_solo",
        "solo_locked.png",
        "solo.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE
                result = 'Victory'
                AND players = 1
        )
        """,
        None,
    ),

    (
        "full_table",
        "full_table_locked.png",
        "full_table.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE
                result = 'Victory'
                AND players = 6
        )
        """,
        None,
    ),


    # =========================================================
    # Number of games
    # =========================================================

    (
        "veteran",
        "veteran_locked.png",
        "veteran.png",
        """
        SELECT COUNT(*) >= 25
        FROM games
        WHERE status = 'FINISHED'
        """,
        None,
    ),

    (
        "legend",
        "legend_locked.png",
        "legend.png",
        """
        SELECT COUNT(*) >= 100
        FROM games
        WHERE status = 'FINISHED'
        """,
        None,
    ),

    (
        "dedicated",
        "dedicated_locked.png",
        "dedicated.png",
        """
        SELECT COUNT(*) >= 50
        FROM games
        WHERE result = 'Victory'
        """,
        None,
    ),


    # =========================================================
    # Score
    # =========================================================

    (
        "high_scorer",
        "score_locked.png",
        "score100.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE score >= 100
        )
        """,
        None,
    ),

    (
        "champion",
        "champion_locked.png",
        "champion.png",
        """
        SELECT COALESCE(SUM(score), 0) >= 1000
        FROM games
        WHERE result = 'Victory'
        """,
        None,
    ),


    # =========================================================
    # Board states
    # =========================================================

    (
        "perfect_island",
        "perfect_locked.png",
        "perfect.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE
                result = 'Victory'
                AND blight_remaining = 0
        )
        """,
        None,
    ),

    (
        "caretaker",
        "caretaker_locked.png",
        "caretaker.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE
                result = 'Victory'
                AND dahan_remaining = players
        )
        """,
        None,
    ),

    (
        "empty_island",
        "empty_locked.png",
        "empty.png",
        """
        SELECT EXISTS(
            SELECT 1
            FROM games
            WHERE
                result = 'Victory'
                AND invader_cards_remaining = 0
        )
        """,
        None,
    ),
]