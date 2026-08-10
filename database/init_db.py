import sqlite3
from pathlib import Path
import argparse
import os

from database.seed_trophies import seed_trophies

from database.config import (
    DATABASE_VERSION,
    DB_NAME,
    DB_PATH
)



# DATA inital of the DB
spirits = [
    "Frappe Cinglante de l'Éclair",
    "Jaillissement de la Rivière Étincelante",
    "Force Vitale de la Terre",
    "Ombre Vacillante de la Flamme",
    "Prolifération de la Verdure Rampante",
    "Voix du Tonnerre",
    "Poigne Vorace de l'Océan",
    "Gardien des Contrées Interdites",
    "Coeur du Feu Sauvage",
    "Porteur de Rêves et de Cauchemars",
    "Serpent Someillant dans les Profondeurs",
    "Jours Brisées qui Déchirent les Cieux",
    "Fascination des Contrées Sauvages",
    "Volcan Dominant l'Île",
    "Regard Implacable du Soleil",
    "Pluie Diluvienne qui Arrose le Monde",
    "Starlight Seeks its Form",
    "Souffle Ténébreux Descendant votre Épine Dorsale",
    "Béhémoth aux Yeux de Braise",
    "Crocs Acérés Tapis sous les Feuilles",
    "Dénicheur de Chemins Imperceptibles",
    "Danse Jusqu'à Faire Trembler la Terre",
    "L'Inébranlable Ténacité de la Pierre",
    "Mémoire du Fond des Âges",
    "Eaux Blessées qui Saignent",
    "Voix Errante qui Attise le Délire",
    "Nuées Accordées à l'Unisson",
    "Fléau Ardent de la Vengeance",
    "Gredin qui Prépare un Mauvais Coup",
    "Sentinelle des Foyers",
    "Linceul de Brume Silencieuse",
    "Convoiteur de Fragments Étincelants de la Terre",
    "La Pourriture qui se Répand régénèrant la terre",
]


adversary_difficulties = [

    ("Le Royaume d'Angleterre", 0, 1),
    ("Le Royaume d'Angleterre", 1, 3),
    ("Le Royaume d'Angleterre", 2, 4),
    ("Le Royaume d'Angleterre", 3, 6),
    ("Le Royaume d'Angleterre", 4, 7),
    ("Le Royaume d'Angleterre", 5, 9),
    ("Le Royaume d'Angleterre", 6, 11),

    ("Le Royaume de Suède", 0, 1),
    ("Le Royaume de Suède", 1, 2),
    ("Le Royaume de Suède", 2, 3),
    ("Le Royaume de Suède", 3, 5),
    ("Le Royaume de Suède", 4, 6),
    ("Le Royaume de Suède", 5, 7),
    ("Le Royaume de Suède", 6, 8),

    ("Le Royaume de France (Colonie de Plantations)", 0, 2),
    ("Le Royaume de France (Colonie de Plantations)", 1, 3),
    ("Le Royaume de France (Colonie de Plantations)", 2, 5),
    ("Le Royaume de France (Colonie de Plantations)", 3, 7),
    ("Le Royaume de France (Colonie de Plantations)", 4, 8),
    ("Le Royaume de France (Colonie de Plantations)", 5, 9),
    ("Le Royaume de France (Colonie de Plantations)", 6, 10),

    ("Le Royaume de Brandebourg-Prusse", 0, 1),
    ("Le Royaume de Brandebourg-Prusse", 1, 2),
    ("Le Royaume de Brandebourg-Prusse", 2, 4),
    ("Le Royaume de Brandebourg-Prusse", 3, 6),
    ("Le Royaume de Brandebourg-Prusse", 4, 7),
    ("Le Royaume de Brandebourg-Prusse", 5, 9),
    ("Le Royaume de Brandebourg-Prusse", 6, 10),

    ("Le Royaume d'Écosse", 0, 1),
    ("Le Royaume d'Écosse", 1, 3),
    ("Le Royaume d'Écosse", 2, 4),
    ("Le Royaume d'Écosse", 3, 6),
    ("Le Royaume d'Écosse", 4, 7),
    ("Le Royaume d'Écosse", 5, 8),
    ("Le Royaume d'Écosse", 6, 10),

    ("Le Tsarat de Russie", 0, 1),
    ("Le Tsarat de Russie", 1, 3),
    ("Le Tsarat de Russie", 2, 4),
    ("Le Tsarat de Russie", 3, 6),
    ("Le Tsarat de Russie", 4, 7),
    ("Le Tsarat de Russie", 5, 9),
    ("Le Tsarat de Russie", 6, 11),

    ("La Monarchie de Habsbourg (Colonie d'Éleveurs)", 0, 2),
    ("La Monarchie de Habsbourg (Colonie d'Éleveurs)", 1, 3),
    ("La Monarchie de Habsbourg (Colonie d'Éleveurs)", 2, 5),
    ("La Monarchie de Habsbourg (Colonie d'Éleveurs)", 3, 6),
    ("La Monarchie de Habsbourg (Colonie d'Éleveurs)", 4, 8),
    ("La Monarchie de Habsbourg (Colonie d'Éleveurs)", 5, 9),
    ("La Monarchie de Habsbourg (Colonie d'Éleveurs)", 6, 10),

    ("L'Expédition Minière des Habsbourg", 0, 1),
    ("L'Expédition Minière des Habsbourg", 1, 3),
    ("L'Expédition Minière des Habsbourg", 2, 4),
    ("L'Expédition Minière des Habsbourg", 3, 5),
    ("L'Expédition Minière des Habsbourg", 4, 7),
    ("L'Expédition Minière des Habsbourg", 5, 9),
    ("L'Expédition Minière des Habsbourg", 6, 10),
]


scenarios = [

    ("Blitz", 0),
    ("Protection du Coeur de l'Île", 0),
    ("Rituels de Terreur", 3),
    ("L'Insurrection des Dahans", 4),

    ("Deuxième Vague", 1),
    ("Puissance Immémoriales", 1),
    ("Protection des Rivages", 2),
    ("Rituels de Purification par les Flammes", 3),

    ("Invocation Élémentaire", 1),
    ("Sa Place est dans un Musée !", 2),
    ("De l'Autre Côté du Fleuve", 3),

    ("Une Diversité d'Esprits", 0),
    ("Terrains Hétérogène", 2),

    ("Le Destin se Révèle", -1),
    ("Vagues de Colonisation", 2),

    ("Protection de la Flamme Sacrée", 1),
]


boards = [

    "Est",
    "Ouest",
    "Nord-Est",
    "Nord-Ouest",
    "Sud-Est",
    "Sud-Ouest",

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

    DROP TABLE IF EXISTS board_configurations;

    DROP TABLE IF EXISTS spirits;
    DROP TABLE IF EXISTS adversaries;
    DROP TABLE IF EXISTS scenarios;
    DROP TABLE IF EXISTS difficulties;
    DROP TABLE IF EXISTS boards;
    DROP TABLE IF EXISTS database_info;
    DROP TABLE IF EXISTS adversary_difficulties;
    DROP TABLE IF EXISTS trophies;

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

    CREATE TABLE trophies (
        id INTEGER PRIMARY KEY,

        name TEXT NOT NULL,
        description TEXT NOT NULL,

        locked_image TEXT NOT NULL,
        unlocked_image TEXT NOT NULL,

        sql_condition TEXT,
        python_condition TEXT,

        CHECK (
            (sql_condition IS NOT NULL AND python_condition IS NULL)
            OR
            (sql_condition IS NULL AND python_condition IS NOT NULL)
        )
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


    for level in range(0,7):

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

    seed_trophies(cursor)


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