from pathlib import Path

DB_NAME = "spirit_island.db"

DATABASE_VERSION = 1

DB_PATH = (
    Path(__file__).parent /
    DB_NAME
)