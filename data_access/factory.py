from pathlib import Path

from config.active import MODE


def create_data_provider(
    user_data_dir,
):

    if MODE == "standalone":

        from database.config import BUNDLED_DB_FILENAME as DB_NAME
        from data_access.sqlite import SQLiteDataProvider

        database_path = Path(user_data_dir) / DB_NAME

        return SQLiteDataProvider(database_path=database_path)

    if MODE == "http":
        from config.http import API_URL
        from data_access.http import HTTPDataProvider

        return HTTPDataProvider(
            base_url=API_URL
        )

    raise ValueError(
        f"Unknown application mode: {MODE}"
    )