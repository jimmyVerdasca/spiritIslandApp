from dataclasses import dataclass, field

from .game_status import GameStatus


@dataclass
class Spirit:
    id: int
    key: str


@dataclass
class Board:

    id: int
    key: str


@dataclass
class BoardConfiguration:
    id: int
    key: str
    min_players: int
    max_players: int


@dataclass
class Adversary:
    id: int
    key: str


@dataclass
class Scenario:
    id: int
    key: str
    score_difficulty: int

@dataclass
class Difficulty:
    id: int
    level: int

@dataclass
class GameAdversary:
    adversary: Adversary
    difficulty: Difficulty

@dataclass
class AdversaryDifficulty:
    adversary: Adversary
    difficulty: Difficulty
    score_difficulty: int

@dataclass
class Game:
    id: int | None = None
    players: int = 0
    configuration: BoardConfiguration | None = None

    spirits: list[Spirit] = field(default_factory=list)
    boards: list[Board] = field(default_factory=list)
    adversaries: list[GameAdversary] = field(default_factory=list)
    scenarios: list[Scenario] = field(default_factory=list)

    status: GameStatus = GameStatus.RUNNING

    result: str | None = None
    score: int | None = None
    invader_cards_remaining: int | None = None
    dahan_remaining: int | None = None
    blight_remaining: int | None = None
    created_at: str | None = None

@dataclass
class Trophy:

    id: int
    key: str

    locked_image: str
    unlocked_image: str

    sql_condition: str | None
    python_condition: str | None

    unlocked: bool = False