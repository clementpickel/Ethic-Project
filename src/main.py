from gomoku import Gomoku
from bot import StupidBot, StupidBot2

if __name__ == "__main__":
    bot1 = StupidBot()
    bot2 = StupidBot2()
    game = Gomoku(bot1, bot2)

    game.game_loop(number_of_moves=10)
    game.print_board()

    print("Winner is", game.winner)
