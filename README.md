# Ethic-Project

To start

```
pip install matplotlib
python src/main.py
```

## Different modes : 

- Human vs bot
  select a bot and play with it
- Bot vs bot
  select two bots and see them fight between each other
- Train with GUI
  train the LearningBot and see the training in the GUI
- Train without GUI
  train the LearningBot and see the

## Threat scores 

To represent our idea of creativity as the threat level of a move for an agent, we created a MoveEvaluation class. This contains multiple functions that are called to check if some patterns exist in the code. It’s simple for now, and check : Open four (four pieces with no enemy pieces at their extremity of the line of pieces), semi-open four (four pieces with just one enemy piece at one of the two extremity of the line of pieces), and the same for 3 pieces and 2 pieces. Each one of these patterns have a different score based on their level of threat, after all being called we got a player score player. Another function plot the evolution of the threat (or creativity) per move of the two players at the end of the game using matplotlib.
