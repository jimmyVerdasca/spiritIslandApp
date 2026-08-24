from pathlib import Path

from shared.database import database
from shared.database.config import BUNDLED_DB_PATH

from .base import DataProvider


class SQLiteDataProvider(DataProvider):

    def __init__(self, database_path: Path):

        self.database_path = Path(
            database_path
        )

        database.ensure_database(
            database_path=self.database_path,
            template_path=BUNDLED_DB_PATH,
        )

        # =================================================
        # Static data cache
        # =================================================

        self._configurations = (
            database.get_configurations(
                self.database_path
            )
        )

        self._spirits = (
            database.get_spirits(
                self.database_path
            )
        )

        self._boards = (
            database.get_boards(
                self.database_path
            )
        )

        self._adversaries = (
            database.get_adversaries(
                self.database_path
            )
        )

        self._difficulties = (
            database.get_difficulties(
                self.database_path
            )
        )

        self._scenarios = (
            database.get_scenarios(
                self.database_path
            )
        )

        self._adversaries_difficulties = (
            database.get_adversaries_difficulties(
                self.database_path
            )
        )

        self._trophies = (
            database.get_trophies(
                self.database_path
            )
        )

    # =================================================
    # Static data
    # =================================================

    @property
    def configurations(self):
        return self._configurations

    @property
    def spirits(self):
        return self._spirits

    @property
    def boards(self):
        return self._boards

    @property
    def adversaries(self):
        return self._adversaries

    @property
    def difficulties(self):
        return self._difficulties

    @property
    def scenarios(self):
        return self._scenarios

    @property
    def adversaries_difficulties(self):
        return self._adversaries_difficulties

    @property
    def trophies(self):
        return self._trophies

    # =================================================
    # Games
    # =================================================

    def save_game(self, game):

        return database.save_game(
            self.database_path,
            game
        )

    def get_running_games(
        self,
        limit=20,
        offset=0,
    ):

        return database.get_running_games(
            self.database_path,
            limit=limit,
            offset=offset,
        )

    def get_finished_games(
        self,
        result=None,
        limit=20,
        offset=0,
    ):

        return database.get_finished_games(
            self.database_path,
            result=result,
            limit=limit,
            offset=offset,
        )

    def get_abandoned_games(
        self,
        limit=20,
        offset=0,
    ):

        return database.get_abandoned_games(
            self.database_path,
            limit=limit,
            offset=offset,
        )

    # =================================================
    # Game state
    # =================================================

    def abandon_game(self, game_id):

        return database.abandon_game(
            self.database_path,
            game_id
        )

    def finish_game(
        self,
        game_id,
        result,
        score,
        invader_cards,
        dahan,
        blight,
    ):

        return database.finish_game(
            self.database_path,
            game_id,
            result,
            score,
            invader_cards,
            dahan,
            blight,
        )