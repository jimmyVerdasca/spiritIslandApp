from enum import Enum


class GameStatus(str, Enum):

    RUNNING = "RUNNING"
    FINISHED = "FINISHED"