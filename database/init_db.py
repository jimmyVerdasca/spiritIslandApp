import sqlite3
from pathlib import Path
import argparse
import os

from database.seed_trophies import seed_trophies

from database.config import (
    DATABASE_VERSION,
    DB_NAME,
    DB_PATH,
)


# =========================================================
# INITIAL DATABASE DATA
# =========================================================

SPIRITS = [
    "lightnings_swift_strike",
    "rivers_surges_in_sunlight",
    "vital_strength_of_the_earth",
    "shadows_flicker_like_flame",
    "a_spreading_rampant_green",
    "thunderspeaker",
    "oceans_hungry_grasp",
    "keeper_of_the_forbidden_wilds",
    "heart_of_the_wildfire",
    "bringer_of_dreams_and_nightmares",
    "serpent_slumbering_beneath_the_island",
    "fractured_days_split_the_sky",
    "lure_of_the_deep_wilderness",
    "volcano_looming_high",
    "shifting_memory_of_ages",
    "downpour_drenches_the_world",
    "starlight_seeks_its_form",
    "darkness_descends_like_a_choking_shroud",
    "eyes_watch_from_the_trees",
    "sharp_fangs_behind_the_leaves",
    "finder_of_paths_unseen",
    "dances_up_earthquakes",
    "stone_unyielding_defiance",
    "memory_of_the_ages",
    "wounded_waters_bleeding",
    "wandering_voice_keens_delirium",
    "many_minds_move_as_one",
    "vengeance_as_a_burning_plague",
    "trickster_plays_a_bad_joke",
    "hearth_vigil",
    "silent_mist",
    "covets_gleaming_shards_of_earth",
    "rot_renews_the_earth",
]


ADVERSARY_DIFFICULTIES = [

    # England

    ("kingdom_of_england", 0, 1),
    ("kingdom_of_england", 1, 3),
    ("kingdom_of_england", 2, 4),
    ("kingdom_of_england", 3, 6),
    ("kingdom_of_england", 4, 7),
    ("kingdom_of_england", 5, 9),
    ("kingdom_of_england", 6, 11),

    # Sweden

    ("kingdom_of_sweden", 0, 1),
    ("kingdom_of_sweden", 1, 2),
    ("kingdom_of_sweden", 2, 3),
    ("kingdom_of_sweden", 3, 5),
    ("kingdom_of_sweden", 4, 6),
    ("kingdom_of_sweden", 5, 7),
    ("kingdom_of_sweden", 6, 8),

    # France

    ("kingdom_of_france", 0, 2),
    ("kingdom_of_france", 1, 3),
    ("kingdom_of_france", 2, 5),
    ("kingdom_of_france", 3, 7),
    ("kingdom_of_france", 4, 8),
    ("kingdom_of_france", 5, 9),
    ("kingdom_of_france", 6, 10),

    # Brandenburg-Prussia

    ("kingdom_of_brandenburg_prussia", 0, 1),
    ("kingdom_of_brandenburg_prussia", 1, 2),
    ("kingdom_of_brandenburg_prussia", 2, 4),
    ("kingdom_of_brandenburg_prussia", 3, 6),
    ("kingdom_of_brandenburg_prussia", 4, 7),
    ("kingdom_of_brandenburg_prussia", 5, 9),
    ("kingdom_of_brandenburg_prussia", 6, 10),

    # Scotland

    ("kingdom_of_scotland", 0, 1),
    ("kingdom_of_scotland", 1, 3),
    ("kingdom_of_scotland", 2, 4),
    ("kingdom_of_scotland", 3, 6),
    ("kingdom_of_scotland", 4, 7),
    ("kingdom_of_scotland", 5, 8),
    ("kingdom_of_scotland", 6, 10),

    # Russia

    ("tsardom_of_russia", 0, 1),
    ("tsardom_of_russia", 1, 3),
    ("tsardom_of_russia", 2, 4),
    ("tsardom_of_russia", 3, 6),
    ("tsardom_of_russia", 4, 7),
    ("tsardom_of_russia", 5, 9),
    ("tsardom_of_russia", 6, 11),

    # Habsburg Livestock Colony

    ("habsburg_livestock_colony", 0, 2),
    ("habsburg_livestock_colony", 1, 3),
    ("habsburg_livestock_colony", 2, 5),
    ("habsburg_livestock_colony", 3, 6),
    ("habsburg_livestock_colony", 4, 8),
    ("habsburg_livestock_colony", 5, 9),
    ("habsburg_livestock_colony", 6, 10),

    # Habsburg Mining Expedition

    ("habsburg_mining_expedition", 0, 1),
    ("habsburg_mining_expedition", 1, 3),
    ("habsburg_mining_expedition", 2, 4),
    ("habsburg_mining_expedition", 3, 5),
    ("habsburg_mining_expedition", 4, 7),
    ("habsburg_mining_expedition", 5, 9),
    ("habsburg_mining_expedition", 6, 10),
]


SCENARIOS = [

    ("blitz", 0),
    ("guard_the_island_heart", 0),
    ("rituals_of_terror", 3),
    ("dahan_insurrection", 4),

    ("second_wave", 1),
    ("rituals_of_destruction", 1),
    ("guard_the_shores", 2),
    ("rituals_of_the_destroying_flames", 3),

    ("elemental_invocation", 1),
    ("its_a_place_of_mystery", 2),
    ("across_the_divide", 3),

    ("diversity_of_spirits", 0),
    ("varied_terrain", 2),

    ("the_destiny_unfolds", -1),
    ("waves_of_colonization", 2),

    ("protect_the_sacred_flame", 1),
]


BOARDS = [
    "east",
    "west",
    "northeast",
    "northwest",
    "southeast",
    "southwest",
]


BOARD_CONFIGURATIONS = [
    (
        "normal",
        2,
        6,
    ),

    (
        "star",
        5,
        5,
    ),
]


# =========================================================
# DATABASE CREATION
# =========================================================

def create_database(path):

    db = sqlite3.connect(path)

    cursor = db.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS game_scenarios;
        DROP TABLE IF EXISTS game_adversaries;
        DROP TABLE IF EXISTS game_boards;
        DROP TABLE IF EXISTS game_spirits;
        DROP TABLE IF EXISTS games;

        DROP TABLE IF EXISTS board_configurations;

        DROP TABLE IF EXISTS spirits;
        DROP TABLE IF EXISTS adversaries;
        DROP TABLE IF EXISTS scenarios;
        DROP TABLE IF EXISTS difficulties;
        DROP TABLE IF EXISTS boards;
        DROP TABLE IF EXISTS adversary_difficulties;
        DROP TABLE IF EXISTS trophies;


        CREATE TABLE spirits(
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE NOT NULL
        );


        CREATE TABLE adversaries(
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE NOT NULL
        );


        CREATE TABLE scenarios(
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE NOT NULL,
            score_difficulty INTEGER NOT NULL
        );


        CREATE TABLE difficulties(
            id INTEGER PRIMARY KEY,
            level INTEGER UNIQUE NOT NULL
        );


        CREATE TABLE boards(
            id INTEGER PRIMARY KEY,
            key TEXT UNIQUE NOT NULL
        );


        CREATE TABLE adversary_difficulties(
            adversary_id INTEGER NOT NULL,
            difficulty_id INTEGER NOT NULL,
            score_difficulty INTEGER NOT NULL,

            PRIMARY KEY(
                adversary_id,
                difficulty_id
            )
        );


        CREATE TABLE board_configurations(

            id INTEGER PRIMARY KEY,

            key TEXT UNIQUE NOT NULL,

            min_players INTEGER NOT NULL,

            max_players INTEGER NOT NULL,

            is_thematic INTEGER NOT NULL DEFAULT 0
        );


        CREATE TABLE trophies (

            id INTEGER PRIMARY KEY,

            key TEXT NOT NULL UNIQUE,

            locked_image TEXT NOT NULL,
            unlocked_image TEXT NOT NULL,

            sql_condition TEXT,
            python_condition TEXT,

            CHECK (
                (
                    sql_condition IS NOT NULL
                    AND python_condition IS NULL
                )
                OR
                (
                    sql_condition IS NULL
                    AND python_condition IS NOT NULL
                )
            )
        );
        """
    )


    # =========================================================
    # SPIRITS
    # =========================================================

    for key in SPIRITS:

        cursor.execute(
            """
            INSERT INTO spirits(key)
            VALUES(?)
            """,
            (key,)
        )


    # =========================================================
    # ADVERSARIES
    # =========================================================

    adversaries = sorted(
        {
            key
            for key, _, _ in ADVERSARY_DIFFICULTIES
        }
    )

    for key in adversaries:

        cursor.execute(
            """
            INSERT INTO adversaries(key)
            VALUES(?)
            """,
            (key,)
        )


    # =========================================================
    # SCENARIOS
    # =========================================================

    for key, score_difficulty in SCENARIOS:

        cursor.execute(
            """
            INSERT INTO scenarios(
                key,
                score_difficulty
            )
            VALUES(?, ?)
            """,
            (
                key,
                score_difficulty,
            )
        )


    # =========================================================
    # BOARDS
    # =========================================================

    for key in BOARDS:

        cursor.execute(
            """
            INSERT INTO boards(key)
            VALUES(?)
            """,
            (key,)
        )


    # =========================================================
    # DIFFICULTIES
    # =========================================================

    for level in range(0, 7):

        cursor.execute(
            """
            INSERT INTO difficulties(level)
            VALUES(?)
            """,
            (level,)
        )


    # =========================================================
    # BOARD CONFIGURATIONS
    # =========================================================

    for key, min_players, max_players in BOARD_CONFIGURATIONS:

        cursor.execute(
            """
            INSERT INTO board_configurations(
                key,
                min_players,
                max_players
            )
            VALUES(?, ?, ?)
            """,
            (
                key,
                min_players,
                max_players,
            )
        )


    # =========================================================
    # HELPERS
    # =========================================================

    def get_adversary_id(key):

        cursor.execute(
            """
            SELECT id
            FROM adversaries
            WHERE key = ?
            """,
            (key,)
        )

        return cursor.fetchone()[0]


    def get_difficulty_id(level):

        cursor.execute(
            """
            SELECT id
            FROM difficulties
            WHERE level = ?
            """,
            (level,)
        )

        return cursor.fetchone()[0]


    # =========================================================
    # ADVERSARY DIFFICULTIES
    # =========================================================

    for adversary_key, level, score_difficulty in ADVERSARY_DIFFICULTIES:

        cursor.execute(
            """
            INSERT INTO adversary_difficulties(
                adversary_id,
                difficulty_id,
                score_difficulty
            )
            VALUES (?, ?, ?)
            """,
            (
                get_adversary_id(adversary_key),
                get_difficulty_id(level),
                score_difficulty,
            )
        )


    # =========================================================
    # GAMES
    # =========================================================

    cursor.execute(
        """
        CREATE TABLE games(

            id INTEGER PRIMARY KEY,

            players INTEGER NOT NULL,

            configuration_id INTEGER NOT NULL,

            status TEXT NOT NULL
                DEFAULT 'RUNNING',

            result TEXT,

            score INTEGER,

            invader_cards_remaining INTEGER,

            dahan_remaining INTEGER,

            blight_remaining INTEGER,

            created_at TEXT NOT NULL
                DEFAULT CURRENT_TIMESTAMP
        );
        """
    )


    cursor.execute(
        """
        CREATE TABLE game_spirits(

            game_id INTEGER NOT NULL,

            spirit_id INTEGER NOT NULL,

            position INTEGER NOT NULL
        );
        """
    )


    cursor.execute(
        """
        CREATE TABLE game_boards(

            game_id INTEGER NOT NULL,

            board_id INTEGER NOT NULL,

            position INTEGER NOT NULL
        );
        """
    )


    cursor.execute(
        """
        CREATE TABLE game_adversaries(

            game_id INTEGER NOT NULL,

            adversary_id INTEGER NOT NULL,

            difficulty_id INTEGER NOT NULL
        );
        """
    )


    cursor.execute(
        """
        CREATE TABLE game_scenarios(

            game_id INTEGER NOT NULL,

            scenario_id INTEGER NOT NULL
        );
        """
    )


    # =========================================================
    # TROPHIES
    # =========================================================

    seed_trophies(cursor)


    # =========================================================
    # COMMIT
    # =========================================================

    db.commit()


    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    )

    print(cursor.fetchall())


    db.close()


    print(
        "Database created:",
        path
    )


    print(
        "Database exists:",
        Path(path).exists()
    )

    print(
        "Database size:",
        Path(path).stat().st_size
    )

    print(
        "Absolute path:",
        Path(path).resolve()
    )


# =========================================================
# APPLICATION DATABASE PATH
# =========================================================

def get_app_database_path():

    data_dir = (
        Path.home()
        / "AppData"
        / "Roaming"
        / "spiritisland"
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return data_dir / DB_NAME


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--app-data",
        action="store_true",
        help="Create database in application data directory"
    )

    args = parser.parse_args()

    if args.app_data:

        path = get_app_database_path()

    else:

        path = DB_PATH


    print(
        f"try create db at {path}"
    )

    create_database(path)