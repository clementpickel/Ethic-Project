from enum import Enum

class GameState(Enum):
    START = 1
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'
    FINISHED = 4

class TurnResult(Enum):
    VALID = 1
    INVALID = 2
    WIN = 3
    DRAW = 4
