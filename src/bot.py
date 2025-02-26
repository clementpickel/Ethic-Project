class Bot:
    def __init__(self):
        pass
    
    def play(self, board: list[list[str]]) -> tuple:
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
