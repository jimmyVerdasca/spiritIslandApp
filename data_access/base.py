from abc import ABC, abstractmethod

from models.game import Game


class DataProvider(ABC):

    @property
    @abstractmethod
    def configurations(self):
        pass

    @property
    @abstractmethod
    def spirits(self):
        pass

    @property
    @abstractmethod
    def boards(self):
        pass

    @property
    @abstractmethod
    def adversaries(self):
        pass

    @property
    @abstractmethod
    def difficulties(self):
        pass

    @property
    @abstractmethod
    def scenarios(self):
        pass

    @property
    @abstractmethod
    def adversaries_difficulties(self):
        pass

    @property
    @abstractmethod
    def trophies(self):
        pass

    # -----------------------------------------
    # Game operations
    # -----------------------------------------

    @abstractmethod
    def save_game(self, game: Game) -> int:
        pass

    @abstractmethod
    def get_running_games(
        self,
        limit=20,
        offset=0,
    ) -> list[Game]:
        pass

    @abstractmethod
    def get_finished_games(
        self,
        result=None,
        limit=20,
        offset=0,
    ) -> list[Game]:
        pass

    @abstractmethod
    def get_abandoned_games(
        self,
        limit=20,
        offset=0,
    ) -> list[Game]:
        pass

    @abstractmethod
    def abandon_game(self, game_id):
        pass

    @abstractmethod
    def finish_game(
        self,
        game_id,
        result,
        score,
        invader_cards,
        dahan,
        blight,
    ):
        pass
