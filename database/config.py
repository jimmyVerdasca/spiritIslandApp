from pathlib import Path

DB_NAME = "spirit_island.db"

DATABASE_VERSION = 2

DB_PATH = (
    Path(__file__).parent /
    DB_NAME
)