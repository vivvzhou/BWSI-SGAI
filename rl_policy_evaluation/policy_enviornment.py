
from enum import IntEnum
import numpy as np

class PolicyEnvironment:
    """
    The 4x4 gridworld shown in Example 4.1.
    """
    state_space = ["zombie", "human", "injured", "corpse"]
    action_space = ["save", "squish", "skip", "scram"]

    def peek(self, remaining_time, humanoid, action):
        """
        Returns the result of taking given action on the given state.
        The result consists of next state and reward.
        """
        reward = 0
        if self.is_done(remaining_time):
            return remaining_time, 0

        if action == "save":
            remaining_time -= 30
            
            if humanoid.is_zombie():
                #self.__ambulance["zombie"] += 1
                reward += 0
            elif humanoid.is_injured():
                #self.__ambulance["injured"] += 1
                reward += 10
            else:
                #self.__ambulance["healthy"] += 1
                reward += 5
        
        elif action == "Action.Squish": #don't keep track of killed or saved because robot does not care, only care about highest score
            remaining_time -= 5
            #if not humanoid.is_zombie():
                #self.__scorekeeper["killed"] += 1
            reward += 0
            
        if action == "Action.Skip": #don't keep track of killed or saved because robot does not care, only care about highest score
            remaining_time -= 15
            #if self.humanoid.is_injured():
                #self.__scorekeeper["killed"] += 1
            reward += 0
            
        if action == "Action.Scram": #notice how robot does not care about scram. Impliment reset
            remaining_time -= 120
            #if self.__ambulance["zombie"] > 0:
                #self.__scorekeeper["killed"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
            #else:
                #self.__scorekeeper["saved"] += self.__ambulance["injured"] + self.__ambulance["healthy"]

            #self.__ambulance["zombie"] = 0
            #self.__ambulance["injured"] = 0
            #self.__ambulance["healthy"] = 0
            reward += 0

        return remaining_time, reward

    def is_done(self, remaining_time):
        """
        Returns True if given state is the terminal state.
        """
        return remaining_time <= 0