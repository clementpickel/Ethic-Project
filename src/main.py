from gomoku import Gomoku
from bot import StupidBot, StupidBot2
from minmax import MinMaxBot
from menum import GameState

if __name__ == "__main__":
    bot1 = MinMaxBot(symbol=GameState.PLAYER_1, depth=2)
    bot2 = StupidBot(symbol=GameState.PLAYER_2)
    game = Gomoku(bot1, bot2)

    game.game_loop(number_of_moves=20) # first move starts the game
    game.print_board()

    if game.winner is None:
        print("Game is a draw")
    else:
        print("Winner is", game.winner.value)
