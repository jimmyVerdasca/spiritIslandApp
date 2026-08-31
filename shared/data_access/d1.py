from shared.database import database
from shared.database.d1_connection import D1Connection
from shared.database.d1_executor import D1Executor

from .base import DataProvider


class D1DataProvider(DataProvider):

    def __init__(
        self,
        account_id,
        database_id,
        api_token,
    ):

        self.connection = D1Connection(
            account_id=account_id,
            database_id=database_id,
            api_token=api_token,
        )

        self.executor = D1Executor(
            self.connection
        )

        # =================================================
        # Static data cache
        # =================================================

        self._configurations = (
            database.get_configurations(
                self.executor
            )
        )

        self._spirits = (
            database.get_spirits(
                self.executor
            )
        )

        self._boards = (
            database.get_boards(
                self.executor
            )
        )

        self._adversaries = (
            database.get_adversaries(
                self.executor
            )
        )

        self._difficulties = (
            database.get_difficulties(
                self.executor
            )
        )

        self._scenarios = (
            database.get_scenarios(
                self.executor
            )
        )

        self._adversaries_difficulties = (
            database.get_adversaries_difficulties(
                self.executor
            )
        )

        self._trophies = (
            database.get_trophies(
                self.executor
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

    def save_game(
        self,
        game,
    ):

        return database.save_game(
            self.executor,
            game,
        )

    def get_running_games(
        self,
        limit=20,
        offset=0,
    ):

        return database.get_running_games(
            self.executor,
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
            self.executor,
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
            self.executor,
            limit=limit,
            offset=offset,
        )

    # =================================================
    # Game state
    # =================================================

    def abandon_game(
        self,
        game_id,
    ):

        return database.abandon_game(
            self.executor,
            game_id,
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
            self.executor,
            game_id,
            result,
            score,
            invader_cards,
            dahan,
            blight,
        )

    # =================================================
    # Lifecycle
    # =================================================

    def close(self):

        self.executor.close()