import sqlite3

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


adversaries = [
    "Angleterre",
    "Suède",
    "France",
    "BrandebourgPrusse",
    "Ecosse",
    "Russie",
    "MonarchieDesHabsbourg",
    "Minier",
]


scenarios = [

    "Blitz",
    "ProtectionDuCoeurDeLÎle",
    "RituelsDeTerreur",
    "InsurrectionDesDahans",

    "DeuxièmeVague",
    "PuissanceImmemoriale",
    "ProtégerLesRivages",
    "RituelsDePurification",

    "InvocationÉlémentaire",
    "PlaceDansUnMusée",
    "DeLautreCotéDuFleuve",

    "DiversitéDesEsprits",
    "TerrainsHétérogène",

    "DestinSeRévèle",
    "VaguesDeColonisation",

    "SaintValentin",
]


boards = [

    "Est",
    "Ouest",
    "NordEst",
    "NordOuest",
    "SudEst",
    "SudOuest",

]

def create_database():
    ''' clean/create db table and populate it with initial datas '''

    db = sqlite3.connect(DB_PATH)

    cursor = db.cursor()


    cursor.executescript("""

    DROP TABLE IF EXISTS configuration_boards;
    DROP TABLE IF EXISTS board_configurations;

    DROP TABLE IF EXISTS spirits;
    DROP TABLE IF EXISTS adversaries;
    DROP TABLE IF EXISTS scenarios;
    DROP TABLE IF EXISTS difficulties;
    DROP TABLE IF EXISTS boards;
    DROP TABLE IF EXISTS database_info;

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
        name TEXT UNIQUE NOT NULL
    );


    CREATE TABLE difficulties(
        id INTEGER PRIMARY KEY,
        level INTEGER UNIQUE NOT NULL
    );


    CREATE TABLE boards(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
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


    for name in adversaries:

        cursor.execute(
            """
            INSERT INTO adversaries(name)
            VALUES(?)
            """,
            (name,)
        )


    for name in scenarios:

        cursor.execute(
            """
            INSERT INTO scenarios(name)
            VALUES(?)
            """,
            (name,)
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



    db.commit()

    db.close()


    print(
        "Database created:",
        DB_PATH
    )



if __name__ == "__main__":

    create_database()