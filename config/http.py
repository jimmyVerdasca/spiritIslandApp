import os
MODE = "http"
API_URL = os.environ.get(
    "SPIRIT_ISLAND_API_URL",
    "https://spirit-island-backend.onrender.com",
)

DB_PROVIDER = os.getenv(
    "SPIRIT_ISLAND_DB_PROVIDER",
    "sqlite",
)