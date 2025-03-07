# training.py
from gomoku import Gomoku
from learning_bot import LearningBot
from menum import GameState

class TrainingManager:
    def __init__(self, bot1, bot2, num_games=1000):
        self.bot1 = bot1
        self.bot2 = bot2
        self.num_games = num_games
        self.win_stats = {'bot1': 0, 'bot2': 0, 'draw': 0}

    def run_training_session(self):
        for game_num in range(self.num_games):
            game = self._play_game()
            self._update_stats(game.winner)
            self._update_bots(game.winner)
            if (game_num + 1) % 100 == 0:
                print(f"After {game_num + 1} games: {self.win_stats}")
        print("Training complete.")
        print("Final Stats:")
        print(f"Bot1 (LearningBot - Player 1) wins: {self.win_stats['bot1']}")
        print(f"Bot2 (LearningBot - Player 2) wins: {self.win_stats['bot2']}")
        print(f"Draws: {self.win_stats['draw']}")

    def _play_game(self):
        game = Gomoku(self.bot1, self.bot2)
        while game.game_state != None and game.winner is None:
            game.game_turn()
        return game

    def _update_stats(self, winner):
        if winner == self.bot1.player:
            self.win_stats['bot1'] += 1
        elif winner == self.bot2.player:
            self.win_stats['bot2'] += 1
        else:
            self.win_stats['draw'] += 1

    def _update_bots(self, winner):
        for bot in [self.bot1, self.bot2]:
            if hasattr(bot, "learn"):
                reward = 1 if winner == bot.player else (-1 if winner else 0)
                bot.learn(reward)
