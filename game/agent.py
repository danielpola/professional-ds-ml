import torch
import random
import numpy as np
from collections import deque
from astro_destroyer import Direction, AstroDestroyer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #popleft()
        
        # TODO: model, trainer
        pass

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    plot_scores = []
    plot_mean_scores =  []
    total_score = 0
    record = 0
    agent = Agent()
    game = AstroDestroyer()
    while True:
        # get current  state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory -> ONLY for one step
        agent.train_short_memory(state_old,
                                    final_move,
                                    reward,
                                    state_new,
                                    done)
        #  remember
        agent.remember(state_old,
                        final_move,
                        reward,
                        state_new,
                        done)
        
        if done:
            #train long memory. Experiene replay / replay memory
            # plot the result
            game.reset()

        # voy en el 54:00. Falta el action en play_step
        # https://www.youtube.com/watch?v=L8ypSXwyBds


if __name__ == '__main__':
    train()