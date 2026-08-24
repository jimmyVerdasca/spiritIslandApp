import os
import shutil

import pytest

from shared.database.config import BUNDLED_DB_PATH


@pytest.fixture(scope="session")
def test_database():
    database_path = os.environ["SPIRIT_ISLAND_DB_PATH"]

    os.makedirs(
        os.path.dirname(database_path),
        exist_ok=True,
    )

    shutil.copy2(
        BUNDLED_DB_PATH,
        database_path,
    )

    return database_path