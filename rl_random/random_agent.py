from enum import IntEnum
import numpy as np
import random
from rl_random.random_action import Action

class RandomAgent:

    def __init__(self, name):
        self.name = name

    def get_action(self):
        random_choice = random.randint(0, 3)
        if (random_choice == 0):
            return "Action.Skip"
        elif (random_choice == 1):
            return "Action.Save"
        elif (random_choice == 2):
            return "Action.Squish"
        else:
            return "Action.Scram"
    
    def update(self, state, action, reward, next_state, done):
        # For training
        pass