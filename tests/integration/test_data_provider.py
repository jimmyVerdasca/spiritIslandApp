from shared.data_access.base import DataProvider
from shared.data_access.factory import create_data_provider
from shared.models.game import Game
from shared.models.game_status import GameStatus


def make_game(provider):
    """
    Build a valid Game using objects loaded from the provider.
    """
    configuration = provider.configurations[0]
    spirit = provider.spirits[0]
    board = provider.boards[0]

    return Game(
        players=2,
        configuration=configuration,
        spirits=[spirit],
        boards=[board],
        adversaries=[],
        scenarios=[],
        status=GameStatus.RUNNING,
    )


def assert_static_data(provider):
    assert isinstance(provider, DataProvider)

    assert provider.configurations
    assert provider.spirits
    assert provider.boards
    assert provider.adversaries
    assert provider.difficulties
    assert provider.scenarios
    assert provider.adversaries_difficulties
    assert provider.trophies


def assert_game_lifecycle(provider):
    game = make_game(provider)

    game_id = provider.save_game(game)

    assert isinstance(game_id, int)
    assert game_id > 0

    running = provider.get_running_games()

    assert any(
        item.id == game_id
        for item in running
    )

    provider.finish_game(
        game_id=game_id,
        result="Victory",
        score=42,
        invader_cards=10,
        dahan=5,
        blight=0,
    )

    running = provider.get_running_games()

    assert not any(
        item.id == game_id
        for item in running
    )

    finished = provider.get_finished_games(
        result="Victory",
    )

    assert any(
        item.id == game_id
        for item in finished
    )


def test_configured_data_provider(backend_server, test_database):
    """
    Test the DataProvider selected by the current application
    configuration.
    """
    provider = create_data_provider(
        application="frontend",
    )

    assert_static_data(provider)
    assert_game_lifecycle(provider)


def test_configured_data_provider_abandon(backend_server, test_database):
    """
    Test game abandonment using the DataProvider selected by the
    current application configuration.
    """
    provider = create_data_provider(
        application="frontend",
    )

    game = make_game(provider)

    game_id = provider.save_game(game)

    running = provider.get_running_games()

    assert any(
        item.id == game_id
        for item in running
    )

    provider.abandon_game(game_id)

    running = provider.get_running_games()

    assert not any(
        item.id == game_id
        for item in running
    )

    abandoned = provider.get_abandoned_games()

    assert any(
        item.id == game_id
        for item in abandoned
    )