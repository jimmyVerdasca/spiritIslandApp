import requests

from models.converters import (
    game_to_json,
    json_to_adversary,
    json_to_adversary_difficulty,
    json_to_board,
    json_to_configuration,
    json_to_difficulty,
    json_to_game,
    json_to_scenario,
    json_to_spirit,
    json_to_trophy,
)

from .base import DataProvider


class HTTPDataProvider(DataProvider):

    def __init__(
        self,
        base_url,
    ):

        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()

        super().__init__()

    # =================================================
    # HTTP
    # =================================================

    def _request(
        self,
        method,
        path,
        *,
        params=None,
        json=None,
    ):

        response = self.session.request(
            method=method,
            url=f"{self.base_url}/{path.lstrip('/')}",
            params=params,
            json=json,
        )

        response.raise_for_status()

        if response.status_code == 204:
            return None

        return response.json()

    def _get(
        self,
        path,
        *,
        params=None,
    ):

        return self._request(
            "GET",
            path,
            params=params,
        )

    def _post(
        self,
        path,
        *,
        json=None,
    ):

        return self._request(
            "POST",
            path,
            json=json,
        )

    # =================================================
    # Static data
    # =================================================

    def _load_configurations(self):

        return [
            json_to_configuration(item)
            for item in self._get(
                "/configurations"
            )
        ]

    def _load_spirits(self):

        return [
            json_to_spirit(item)
            for item in self._get(
                "/spirits"
            )
        ]

    def _load_boards(self):

        return [
            json_to_board(item)
            for item in self._get(
                "/boards"
            )
        ]

    def _load_adversaries(self):

        return [
            json_to_adversary(item)
            for item in self._get(
                "/adversaries"
            )
        ]

    def _load_difficulties(self):

        return [
            json_to_difficulty(item)
            for item in self._get(
                "/difficulties"
            )
        ]

    def _load_scenarios(self):

        return [
            json_to_scenario(item)
            for item in self._get(
                "/scenarios"
            )
        ]

    def _load_adversaries_difficulties(self):

        return [
            json_to_adversary_difficulty(item)
            for item in self._get(
                "/adversaries-difficulties"
            )
        ]

    def _load_trophies(self):

        return [
            json_to_trophy(item)
            for item in self._get(
                "/trophies"
            )
        ]

    # =================================================
    # Games
    # =================================================

    def save_game(
        self,
        game,
    ):

        data = self._post(
            "/games",
            json=game_to_json(game),
        )

        return data["id"]

    def get_running_games(
        self,
        limit=20,
        offset=0,
    ):

        data = self._get(
            "/games/running",
            params={
                "limit": limit,
                "offset": offset,
            },
        )

        return [
            json_to_game(item)
            for item in data
        ]

    def get_finished_games(
        self,
        result=None,
        limit=20,
        offset=0,
    ):

        params = {
            "limit": limit,
            "offset": offset,
        }

        if result is not None:
            params["result"] = result

        data = self._get(
            "/games/finished",
            params=params,
        )

        return [
            json_to_game(item)
            for item in data
        ]

    def get_abandoned_games(
        self,
        limit=20,
        offset=0,
    ):

        data = self._get(
            "/games/abandoned",
            params={
                "limit": limit,
                "offset": offset,
            },
        )

        return [
            json_to_game(item)
            for item in data
        ]

    # =================================================
    # Game state
    # =================================================

    def abandon_game(
        self,
        game_id,
    ):

        return self._post(
            f"/games/{game_id}/abandon"
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

        return self._post(
            f"/games/{game_id}/finish",
            json={
                "result": result,
                "score": score,
                "invader_cards": invader_cards,
                "dahan": dahan,
                "blight": blight,
            },
        )