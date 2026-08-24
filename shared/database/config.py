from pathlib import Path
import os

DATABASE_VERSION = 2

BUNDLED_DB_FILENAME = (
    "spirit_island.db"
)

BUNDLED_DB_PATH = (
    Path(__file__).parent /
    BUNDLED_DB_FILENAME
)

DB_PATH = os.environ.get(
    "SPIRIT_ISLAND_DB_PATH"
)