from pathlib import Path

from config.active import MODE


def create_data_provider(
    user_data_dir=None,
    application="frontend",
):
    if application == "backend":

        from shared.database.config import BUNDLED_DB_PATH
        from shared.data_access.sqlite import SQLiteDataProvider

        return SQLiteDataProvider(
            database_path=BUNDLED_DB_PATH,
        )

    if application == "frontend":

        if MODE == "standalone":

            from shared.database.config import (
                BUNDLED_DB_FILENAME
            )
            from shared.data_access.sqlite import (
                SQLiteDataProvider
            )

            database_path = (
                Path(user_data_dir)
                / BUNDLED_DB_FILENAME
            )

            return SQLiteDataProvider(
                database_path=database_path,
            )

        if MODE == "http":

            from config.http import API_URL
            from shared.data_access.http import (
                HTTPDataProvider
            )

            return HTTPDataProvider(
                base_url=API_URL,
            )

    raise ValueError(
        f"Unknown application/mode combination: "
        f"{application}/{MODE}"
    )