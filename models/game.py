from dataclasses import dataclass, field

from .game_status import GameStatus


@dataclass
class Spirit:
    id: int
    name: str


@dataclass
class Board:

    id: int
    name: str


@dataclass
class BoardConfiguration:
    id: int
    name: str
    min_players: int
    max_players: int


@dataclass
class Adversary:
    id: int
    name: str


@dataclass
class Scenario:
    id: int
    name: str

@dataclass
class GameAdversary:
    adversary: Adversary
    difficulty: int

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