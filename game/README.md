# Agent

* game
* model

## Training

* state = get_state(game)
* action = get_move(state):
    * model.predict()
* reward, game_over, score = game.play_step(action)
* new_state = get_state(game)
* remember
* model.train()

# Game (PyGame)

* play_state(action)
    * reward, game_over, score

# Model (PyTorch)

* Linear_QNet(DQN)
    * model.predict(state)
        * action