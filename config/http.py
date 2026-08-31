import os
MODE = "http"
API_URL = os.environ.get(
    "SPIRIT_ISLAND_API_URL",
    "http://192.168.1.140:8000",
)

DB_PROVIDER = os.getenv(
    "SPIRIT_ISLAND_DB_PROVIDER",
    "sqlite",
)