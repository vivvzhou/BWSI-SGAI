import copy
from enum import IntEnum
from operator import index
import random
import numpy as np
from td_learning.ql_argmax import QLargmax_all
from td_learning.ql_enviornment import QLEnvironment
from td_learning.ql_role_meter import role_meter
import os

class QLAgent:
    def __init__(self, state_space, time_space, hp_space, capacity_space, role_space, roleMeter_space, action_space, epsilon=0.1, learning_rate=0.1, discount_factor=1, is_training = False):
        """
        Initialize Q table and save environment.
        """
        self.state_space = state_space
        self.time_space = time_space
        self.hp_space = hp_space
        self.action_space = action_space
        self.is_training = is_training
        self.capacity_space = capacity_space
        self.role_space = role_space
        self.roleMeter_space = roleMeter_space #list of "boolean" arrays
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.q_table = np.zeros((len(state_space), len(time_space), len(hp_space), len(capacity_space), len(role_space), len(roleMeter_space), len(action_space)),
                                dtype=float) #initialize Q-table to all zero's for a fresh start when training

        if is_training == False: #read in the Q-table from the data file only when running normally
            code_dir = os.path.dirname(__file__)
            file_path = os.path.join(code_dir, "q_table.txt")
            f = open(file_path, "r") #open file in read only
            for state in range(len(self.q_table)): #read the file and insert the data into the q_table variable
                for time in range(len(self.q_table[state])):
                    for hp in range(len(self.q_table[state][time])):
                        for cap in range(len(self.q_table[state][time][hp])):
                            for rol in range(len(self.q_table[state][time][hp][cap])):
                                for roleMeters in range(len(self.q_table[state][time][hp][cap][rol])):
                                    row = f.readline()
                                    rowList = row.split(" ")
                                    rowList.pop()
                                    for action in range(5):
                                        #print(rowList)
                                        self.q_table[state][time][hp][cap][rol][roleMeters][action] = rowList[action]

    def get_state_role(self):
        """
        Returns random state
        """
        state_index = random.randint(0, len(self.state_space) - 1)
        role_index = random.randint(0, len(self.role_space) - 1)
        return self.state_space[state_index], self.role_space[role_index]
    
    def get_action(self, state, time, hp, capacity, role, roleMeter):
        """
        Returns action based on Q table and epsilon-greedy policy.
        """
        #print(hp)
        rand = np.random.random()
        #print(str(rand) + " " + str(self.epsilon))

        save = True
        squish = True
        skip = True
        cure = True
        scram = True
        
        #Should always be able to skip or scram no matter what to spend the last few minutes
        if hp <= 0:
            squish = False
        if capacity <= 0:
            save = False
            cure = False
        if time < 5:
            squish = False
        #if time < 15:
        #    skip = False
        if time < 30:
            save = False
        if time < 60:
            cure = False
        # if time < 120:
        #     scram = False
            
        roleMeterIndex = self.get_roleMeter_index(roleMeter)

        if rand < self.epsilon and self.is_training: #explore (can only explore when training)
            actions = []
            if save:
                actions.append(self.action_space[0])
            if squish:
                actions.append(self.action_space[1])
            if skip:
                actions.append(self.action_space[2])
            if cure:
                actions.append(self.action_space[3])
            if scram:
                actions.append(self.action_space[4])     
            return np.random.choice(actions)
        
        else: #exploit (can exploit while training and while running)
            actions = []
            for i in self.q_table[state][time//5][hp][capacity][role][roleMeterIndex]: #make a "shallow copy" of the action q_table for that state
                actions.append(i) #shallow copy WITH all actions
            if not save:
                actions[0] = -10000000
            if not squish:
                actions[1] = -10000000
            if not skip:
                actions[2] = -10000000
            if not cure:
                actions[3] = -10000000
            if not scram:
                actions[4] = -10000000
            
            largest = max(actions)
            index = 0
            best_action = []
            for i in actions:
                if i == largest:
                    best_action.append(index)
                index += 1
            return np.random.choice(best_action)
                
            #best_action = QLargmax_all(actions) #get the best action based off the q_table
            #return np.random.choice(best_action)   
        
    def update_q(self, state, time, hp, capacity, role, roleMeter, action, reward, next_state, next_time, next_hp, next_capacity, next_role, next_roleMeter, done):
        """
        Update Q table via Q-Learning.
        """
        roleMeterIndex = self.get_roleMeter_index(roleMeter)
        next_roleMeterIndex = self.get_roleMeter_index(next_roleMeter)
        if done:
            target = reward
        else: #bellman equation
            target = reward + self.discount_factor * \
                np.max(self.q_table[next_state][next_time//5][next_hp][next_capacity][next_role][next_roleMeterIndex])
            #print(target)
        self.q_table[int(state)][int(time//5)][int(hp)][int(capacity)][int(role)][int(roleMeterIndex)][int(action)] += self.learning_rate * \
        (target - self.q_table[int(state)][int(time//5)][int(hp)][int(capacity)][int(role)][int(roleMeterIndex)][int(action)])
        #print(self.q_table[int(state)][int(time//5)][int(hp)][int(capacity)][int(role)][int(roleMeterIndex)][int(action)])
    
    def reset(self):
        #self.q_table = np.zeros((len(QLEnvironment.state_space), len(QLEnvironment.action_space)),       getting error AttributeError: type object 'QLEnvironment' has no attribute 'state_space'
        #                        dtype=float)
        self.q_table = np.zeros((len(self.state_space), len(self.time_space), len(self.hp_space), len(self.capacity_space), len(self.role_space), len(self.roleMeter_space), len(self.action_space)),
                                dtype=float)

    def get_roleMeter_index(self, roleMeter):
        index = 0
        for i in self.roleMeter_space:
            if roleMeter.engineer == i.engineer and roleMeter.teacher == i.teacher and roleMeter.mayor == i.mayor: 
            #and roleMeter.farmer == i.farmer and roleMeter.doctor == i.doctor and roleMeter.criminal == i.criminal:
                return index
            index += 1
        return -1