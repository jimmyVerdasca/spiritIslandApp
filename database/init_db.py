import sqlite3
from pathlib import Path
import argparse
import os

from database.config import (
    DATABASE_VERSION,
    DB_NAME,
    DB_PATH
)



# DATA inital of the DB
spirits = [

    # Base
    "FrappeFoudroyanteDeLEclair",
    "RivièreDéverseSesFlotsEnPleinJour",
    "ForceVitaleDeLaTerre",
    "OmbresFlamboyantes",
    "UnePropagationDeVerdureRampante",
    "TonnerreParleÀTraversLesArbres",

    # Branche et Griffes
    "GardienneDesÎlesOubliées",
    "CoeurDuFeuSacré",
    "PorteurDesRêvesEtDesCauchemars",
    "SerpentSomnolentSousLaSurfaceDuMonde",

    # Jagged Earth
    "BourrasqueDeFoudreDansante",
    "FléauDesOcéansDéchaînés",
    "VolcanQuiSurgitDesProfondeurs",
    "AubeAuxYeuxOuverts",
    "PluieDeLumièreEtDeChaleur",
    "FrissonsDansLesBois",
    "DévorationDesContréesDévastées",
    "RacinesQuiS'ÉtendentPartout",

    # Nature Incarnate
    "GriffesDeLaNatureSauvage",
    "GardienDesSentiersInexplorés",
    "PrésenceÉternelleDeLaForêt",
    "FaimInsatiableDeLIntérieurDeLaTerre",
    "ChantDeLaTerreEnColère",
    "LaSourceDeLaVie",
    "RêveurDeLaContréeÉternelle",

    # Horizons
    "NuageDeRêvesQuiDansent",
    "LézardDeLaFlammeÉternelle",
    "EspritDeLaMontagneÉlevée",
    "ÂmeDeLaForêtProfonde",
    "BrumeQuiS'ÉpaissitEtDisparaît",

    # Custom
    "Dragon",
    "Moisissure",
]


adversary_difficulties = [

    ("Angleterre", 1, 2),
    ("Angleterre", 2, 3),
    ("Angleterre", 3, 6),
    ("Angleterre", 4, 7),
    ("Angleterre", 5, 9),
    ("Angleterre", 6, 11),

    ("Suède", 1, 2),
    ("Suède", 2, 3),
    ("Suède", 3, 5),
    ("Suède", 4, 6),
    ("Suède", 5, 7),
    ("Suède", 6, 8),

    ("France", 1, 3),
    ("France", 2, 5),
    ("France", 3, 7),
    ("France", 4, 8),
    ("France", 5, 9),
    ("France", 6, 10),

    ("BrandebourgPrusse", 1, 2),
    ("BrandebourgPrusse", 2, 4),
    ("BrandebourgPrusse", 3, 6),
    ("BrandebourgPrusse", 4, 8),
    ("BrandebourgPrusse", 5, 10),
    ("BrandebourgPrusse", 6, 12),

    ("Ecosse", 1, 2),
    ("Ecosse", 2, 4),
    ("Ecosse", 3, 6),
    ("Ecosse", 4, 8),
    ("Ecosse", 5, 10),
    ("Ecosse", 6, 11),

    ("Russie", 1, 3),
    ("Russie", 2, 5),
    ("Russie", 3, 7),
    ("Russie", 4, 9),
    ("Russie", 5, 10),
    ("Russie", 6, 11),

    ("MonarchieDesHabsbourg", 1, 3),
    ("MonarchieDesHabsbourg", 2, 5),
    ("MonarchieDesHabsbourg", 3, 6),
    ("MonarchieDesHabsbourg", 4, 8),
    ("MonarchieDesHabsbourg", 5, 9),
    ("MonarchieDesHabsbourg", 6, 10),

    ("Minier", 1, 2),
    ("Minier", 2, 4),
    ("Minier", 3, 6),
    ("Minier", 4, 7),
    ("Minier", 5, 9),
    ("Minier", 6, 10),
]


scenarios = [

    ("Blitz", 0),
    ("ProtectionDuCoeurDeLÎle", 1),
    ("RituelsDeTerreur", 2),
    ("InsurrectionDesDahans", 4),

    ("DeuxièmeVague", 2),
    ("PuissanceImmemoriale", 3),
    ("ProtégerLesRivages", 1),
    ("RituelsDePurification", 2),

    ("InvocationÉlémentaire", 2),
    ("PlaceDansUnMusée", 1),
    ("DeLautreCotéDuFleuve", 1),

    ("DiversitéDesEsprits", 2),
    ("TerrainsHétérogène", 1),

    ("DestinSeRévèle", 2),
    ("VaguesDeColonisation", 3),

    ("SaintValentin", 0),
]


boards = [

    "Est",
    "Ouest",
    "NordEst",
    "NordOuest",
    "SudEst",
    "SudOuest",

]

def create_database(path):
    ''' clean/create db table and populate it with initial datas '''

    db = sqlite3.connect(path)

    cursor = db.cursor()


    cursor.executescript("""
    DROP TABLE IF EXISTS game_scenarios;
    DROP TABLE IF EXISTS game_adversaries;
    DROP TABLE IF EXISTS game_boards;
    DROP TABLE IF EXISTS game_spirits;
    DROP TABLE IF EXISTS games;

    DROP TABLE IF EXISTS configuration_boards;
    DROP TABLE IF EXISTS board_configurations;

    DROP TABLE IF EXISTS spirits;
    DROP TABLE IF EXISTS adversaries;
    DROP TABLE IF EXISTS scenarios;
    DROP TABLE IF EXISTS difficulties;
    DROP TABLE IF EXISTS boards;
    DROP TABLE IF EXISTS database_info;
    DROP TABLE IF EXISTS adversary_difficulties;

    CREATE TABLE database_info(
        version INTEGER NOT NULL
    );

    CREATE TABLE spirits(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    );


    CREATE TABLE adversaries(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    );


    CREATE TABLE scenarios(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        score_difficulty INTEGER NOT NULL
    );


    CREATE TABLE difficulties(
        id INTEGER PRIMARY KEY,
        level INTEGER UNIQUE NOT NULL
    );


    CREATE TABLE boards(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE adversary_difficulties(
        adversary_id INTEGER NOT NULL,
        difficulty_id INTEGER NOT NULL,
        score_difficulty INTEGER NOT NULL,

        PRIMARY KEY(adversary_id, difficulty_id)
    );


    CREATE TABLE board_configurations(

        id INTEGER PRIMARY KEY,

        name TEXT UNIQUE NOT NULL,

        min_players INTEGER NOT NULL,

        max_players INTEGER NOT NULL
    );


    CREATE TABLE configuration_boards(

        configuration_id INTEGER,

        board_id INTEGER,

        position INTEGER
    );


    """)

    cursor.execute(
        """
        INSERT INTO database_info(version)
        VALUES(1)
        """
    )

    cursor.execute(
        f"PRAGMA user_version = {DATABASE_VERSION}"
    )



    for name in spirits:

        cursor.execute(
            """
            INSERT INTO spirits(name)
            VALUES(?)
            """,
            (name,)
        )


    adversaries = sorted({
        name
        for name, _, _ in adversary_difficulties
    })
    
    for name in adversaries:

        cursor.execute(
            """
            INSERT INTO adversaries(name)
            VALUES(?)
            """,
            (name,)
        )


    for name, score_difficulty in scenarios:

        cursor.execute(
            """
            INSERT INTO scenarios(name, score_difficulty)
            VALUES(?, ?)
            """,
            (name, score_difficulty)
        )


    for name in boards:

        cursor.execute(
            """
            INSERT INTO boards(name)
            VALUES(?)
            """,
            (name,)
        )


    for level in range(1,7):

        cursor.execute(
            """
            INSERT INTO difficulties(level)
            VALUES(?)
            """,
            (level,)
        )


    # Board configurations

    cursor.execute(
        """
        INSERT INTO board_configurations
        (
            name,
            min_players,
            max_players
        )
        VALUES
        (
            'Normal',
            2,
            6
        )
        """
    )


    normal_id = cursor.lastrowid



    cursor.execute(
        """
        INSERT INTO board_configurations
        (
            name,
            min_players,
            max_players
        )
        VALUES
        (
            'Étoile',
            5,
            5
        )
        """
    )


    etoile_id = cursor.lastrowid

    def get_adversary_id(name):
        
        cursor.execute(
            """
            SELECT id
            FROM adversaries
            WHERE name = ?
            """,
            (name,)
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

    def get_board_id(name):

        cursor.execute(
            """
            SELECT id
            FROM boards
            WHERE name=?
            """,
            (name,)
        )

        return cursor.fetchone()[0]

    for adversary_name, level, score_difficulty in adversary_difficulties:
    
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
                get_adversary_id(adversary_name),
                get_difficulty_id(level),
                score_difficulty,
            )
        )

    for position, board in enumerate(
        boards,
        start=1
    ):

        cursor.execute(
            """
            INSERT INTO configuration_boards
            VALUES(?,?,?)
            """,
            (
                normal_id,
                get_board_id(board),
                position
            )
        )



    for position, board in enumerate(
        [
            "Est",
            "NordEst",
            "NordOuest",
            "Ouest",
            "SudEst"
        ],
        start=1
    ):

        cursor.execute(
            """
            INSERT INTO configuration_boards
            VALUES(?,?,?)
            """,
            (
                etoile_id,
                get_board_id(board),
                position
            )
        )
        
    cursor.execute(
        """
        CREATE TABLE games(
            id INTEGER PRIMARY KEY,
            players INTEGER NOT NULL,
            configuration_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'RUNNING',
            result TEXT,
            score INTEGER,
            invader_cards_remaining INTEGER,
            dahan_remaining INTEGER,
            blight_remaining INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );"""
    )

    cursor.execute(
        """
        CREATE TABLE game_spirits(
            game_id INTEGER NOT NULL,
            spirit_id INTEGER NOT NULL,
            position INTEGER NOT NULL
        );"""
    )

    cursor.execute(
        """
        CREATE TABLE game_boards(
            game_id INTEGER NOT NULL,
            board_id INTEGER NOT NULL,
            position INTEGER NOT NULL
        );"""
    )

    cursor.execute(
        """
        CREATE TABLE game_adversaries(
            game_id INTEGER NOT NULL,
            adversary_id INTEGER NOT NULL,
            difficulty_id INTEGER NOT NULL
        );"""
    )

    cursor.execute(
        """
        CREATE TABLE game_scenarios(
            game_id INTEGER NOT NULL,
            scenario_id INTEGER NOT NULL
        );
        """
    )


    db.commit()

    cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """
    )

    print(cursor.fetchall())

    db.close()


    print(
        "Database created:",
        path
    )


    print("Database exists:", Path(path).exists())
    print("Database size:", Path(path).stat().st_size)
    print("Absolute path:", Path(path).resolve())

    print(
        "Database created:",
        path
    )

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


    print(f"try create db at {path}")
    create_database(path)