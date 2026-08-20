from pathlib import Path

DATABASE_VERSION = 2

BUNDLED_DB_FILENAME = (
    "spirit_island.db"
)

BUNDLED_DB_PATH = (
    Path(__file__).parent /
    BUNDLED_DB_FILENAME
)