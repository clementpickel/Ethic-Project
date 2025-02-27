from menum import GameState

class Bot:
    def __init__(self, symbol: GameState):
        self.player = symbol
        self.opponent = GameState.PLAYER_1 if symbol == GameState.PLAYER_2 else GameState.PLAYER_2
        pass
    
    def play(self, board: list[list[str]]) -> tuple: #take the board as input and return the move as a tuple
        pass

class StupidBot(Bot):
    def play(self, board: list[list[str]]) -> tuple:
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell is None:
                    return i, j
                
class StupidBot2(Bot):
    def play(self, board: list[list[str]]) -> tuple:
        for i, row in reversed(list(enumerate(board))):
            for j, cell in reversed(list(enumerate(row))):
                if cell is None:
                    return i, j
