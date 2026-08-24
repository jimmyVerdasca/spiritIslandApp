from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


# =========================================================
# Static data
# =========================================================


def test_configurations():
    response = client.get("/configurations")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data

    for item in data:
        assert "id" in item
        assert "key" in item
        assert "min_players" in item
        assert "max_players" in item


def test_spirits():
    response = client.get("/spirits")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data

    for item in data:
        assert "id" in item
        assert "key" in item


def test_boards():
    response = client.get("/boards")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data

    for item in data:
        assert "id" in item
        assert "key" in item


def test_adversaries():
    response = client.get("/adversaries")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data

    for item in data:
        assert "id" in item
        assert "key" in item


def test_difficulties():
    response = client.get("/difficulties")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data

    for item in data:
        assert "id" in item
        assert "level" in item


def test_scenarios():
    response = client.get("/scenarios")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data

    for item in data:
        assert "id" in item
        assert "key" in item
        assert "score_difficulty" in item


def test_adversaries_difficulties():
    response = client.get(
        "/adversaries-difficulties"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_trophies():
    response = client.get("/trophies")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data

    for item in data:
        assert "id" in item
        assert "key" in item


# =========================================================
# Games
# =========================================================


def make_game_payload():
    return {
        "players": 2,
        "configuration": {
            "id": 1,
            "key": "normal",
            "min_players": 2,
            "max_players": 6,
        },
        "spirits": [
            {
                "id": 1,
                "key": "lightnings_swift_strike",
            }
        ],
        "boards": [
            {
                "id": 1,
                "key": "east",
            }
        ],
        "adversaries": [],
        "scenarios": [],
        "status": "RUNNING",
    }


def test_create_game():
    response = client.post(
        "/games",
        json=make_game_payload(),
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["id"] > 0


def test_created_game_appears_in_running_games():
    create_response = client.post(
        "/games",
        json=make_game_payload(),
    )

    assert create_response.status_code == 200

    game_id = create_response.json()["id"]

    response = client.get(
        "/games/running"
    )

    assert response.status_code == 200

    game_ids = [
        game["id"]
        for game in response.json()
    ]

    assert game_id in game_ids


def test_game_can_be_finished():
    create_response = client.post(
        "/games",
        json=make_game_payload(),
    )

    assert create_response.status_code == 200

    game_id = create_response.json()["id"]

    response = client.post(
        f"/games/{game_id}/finish",
        json={
            "result": "Victory",
            "score": 42,
            "invader_cards": 10,
            "dahan": 5,
            "blight": 0,
        },
    )

    assert response.status_code in (200, 204)

    running_response = client.get(
        "/games/running"
    )

    assert running_response.status_code == 200

    running_ids = [
        game["id"]
        for game in running_response.json()
    ]

    assert game_id not in running_ids

    finished_response = client.get(
        "/games/finished",
        params={"result": "Victory"},
    )

    assert finished_response.status_code == 200

    finished_ids = [
        game["id"]
        for game in finished_response.json()
    ]

    assert game_id in finished_ids


def test_game_can_be_abandoned():
    create_response = client.post(
        "/games",
        json=make_game_payload(),
    )

    assert create_response.status_code == 200

    game_id = create_response.json()["id"]

    response = client.post(
        f"/games/{game_id}/abandon"
    )

    assert response.status_code in (200, 204)

    running_response = client.get(
        "/games/running"
    )

    assert running_response.status_code == 200

    running_ids = [
        game["id"]
        for game in running_response.json()
    ]

    assert game_id not in running_ids

    abandoned_response = client.get(
        "/games/abandoned"
    )

    assert abandoned_response.status_code == 200

    abandoned_ids = [
        game["id"]
        for game in abandoned_response.json()
    ]

    assert game_id in abandoned_ids