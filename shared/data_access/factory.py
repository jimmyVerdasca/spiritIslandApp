import os
from pathlib import Path


from config.active import MODE


def create_data_provider(
    user_data_dir=None,
    application="frontend",
):
    if application == "backend":
    
        provider = os.getenv(
            "SPIRIT_ISLAND_DB_PROVIDER",
            "sqlite",
        )

        if provider == "d1":

            from shared.data_access.d1 import (
                D1DataProvider
            )

            return D1DataProvider(
                account_id=os.environ[
                    "CLOUDFLARE_ACCOUNT_ID"
                ],
                api_token=os.environ[
                    "CLOUDFLARE_API_TOKEN"
                ],
                database_id=os.environ[
                    "CLOUDFLARE_D1_DATABASE_ID"
                ],
            )

        if provider == "sqlite":

            from shared.database.config import (
                BUNDLED_DB_PATH,
                DB_PATH,
            )

            from shared.data_access.sqlite import (
                SQLiteDataProvider
            )

            database_path = (
                DB_PATH
                if DB_PATH is not None
                else BUNDLED_DB_PATH
            )

            return SQLiteDataProvider(
                database_path=database_path,
            )

        raise ValueError(
            f"Unknown backend database provider: "
            f"{provider}"
        )

    if application == "frontend":

        if MODE == "standalone":

            from shared.database.config import (
                BUNDLED_DB_FILENAME,
                DB_PATH,
            )
            from shared.data_access.sqlite import (
                SQLiteDataProvider
            )

            database_path = (
                DB_PATH
                if DB_PATH is not None
                else (
                    Path(user_data_dir)
                    / BUNDLED_DB_FILENAME
                )
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