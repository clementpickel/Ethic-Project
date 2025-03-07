# genetic_algorithm.py
import random

def evaluate_bot(bot, num_games=10, opponent_class=None, symbol=None, board_size=15):
    wins = 0
    from gomoku import Gomoku
    from bot import StupidBot
    if opponent_class is None:
        opponent_class = StupidBot
    from constants import GameState
    if symbol is None:
        symbol = GameState.PLAYER_1
    for _ in range(num_games):
        if random.random() < 0.5:
            bot1 = bot
            bot2 = opponent_class(symbol=GameState.PLAYER_2 if symbol == GameState.PLAYER_1 else GameState.PLAYER_1)
        else:
            bot1 = opponent_class(symbol=symbol)
            bot2 = bot
        game = Gomoku(bot1, bot2, size=board_size)
        game.game_loop(number_of_moves=200)
        if game.winner == bot.player:
            wins += 1
    return wins

def crossover(q_table1, q_table2):
    new_q = {}
    keys = set(q_table1.keys()).union(q_table2.keys())
    for key in keys:
        if key in q_table1 and key in q_table2:
            new_q[key] = (q_table1[key] + q_table2[key]) / 2
        elif key in q_table1:
            new_q[key] = q_table1[key]
        else:
            new_q[key] = q_table2[key]
    return new_q

def mutate(q_table, mutation_rate=0.05):
    new_q = {}
    for key, value in q_table.items():
        if random.random() < mutation_rate:
            new_q[key] = value + random.uniform(-1, 1)
        else:
            new_q[key] = value
    return new_q

def evolve_population(population, fitnesses, retain_rate=0.2, mutation_rate=0.05):
    sorted_population = [bot for _, bot in sorted(zip(fitnesses, population), key=lambda x: x[0], reverse=True)]
    retain_length = int(len(sorted_population) * retain_rate)
    survivors = sorted_population[:retain_length]
    children = []
    while len(children) < len(population) - retain_length:
        parent1, parent2 = random.sample(survivors, 2)
        child_q = crossover(parent1.q_table, parent2.q_table)
        child_q = mutate(child_q, mutation_rate)
        from learning_bot import LearningBot
        child = LearningBot(symbol=parent1.player, q_table=child_q,
                            learning_rate=parent1.learning_rate,
                            discount_factor=parent1.discount_factor,
                            exploration_rate=parent1.exploration_rate,
                            exploration_decay=parent1.exploration_decay)
        children.append(child)
    return survivors + children
