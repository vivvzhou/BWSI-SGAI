import copy
from enum import IntEnum
import numpy as np
from td_learning.ql_role_meter import role_meter
import matplotlib.pyplot as plt
import os

#from td_learning.ql_train import run

def runs(env, time, hp, capacity, agent, is_evaluating):
    env.reset(time, hp, capacity)
    done = False
    total_reward = 0
    total_score = 0
    state, role = agent.get_state_role()
    base_capaicty = capacity
    roleMeter = role_meter(False, False, False
    # , False, False, False
    )
    timeData = []
    scoreData = []
    rewardData = []

    while not done: #play thru the game
        timeData.append(time)
        scoreData.append(total_score)
        rewardData.append(total_reward)

        action = agent.get_action(state, time, hp, capacity, role, roleMeter) #get the action (dependent on epsilon, using epsilon-greedy algorithm)
        
        stateWord = ""
        if state == 0:
            stateWord = "zombie"
        elif state == 1:
            stateWord = "healthy"
        elif state == 2:
            stateWord = "injured"
        else:
            stateWord = "corpse"
            
        roleWord = ""
        if role == 0: 
            roleWord = "engineer"
        elif role == 1:
            roleWord = "teacher"
        elif role == 2:
            roleWord = "mayor"
        elif role == 3:
            roleWord = "farmer"
        elif role == 4:
            roleWord = "doctor"
        elif role == 5:
            roleWord = "criminal"
        
        actionWord = ""
        if action == 0:
            actionWord = "save"
        elif action == 1:
            actionWord = "squish"
        elif action == 2:
            actionWord = "skip"
        elif action == 3:
            actionWord = "cure"
        elif action == 4:
            actionWord = "scram"
        

        next_state, next_time, next_hp, next_capacity, next_role, next_roleMeter, reward, score, done = env.step(action, state, role, roleMeter, base_capaicty) #step the environment using the action
        total_reward += reward
        total_score += score
        capacity = next_capacity
        state = next_state #update state
        time = next_time
        role = next_role
        roleMeter = copy.copy(next_roleMeter)
        hp = next_hp
        string = ""
        if roleMeter.engineer == True:
            string += "T"
        else:
            string += "F"

        if roleMeter.teacher == True:
            string += "T"
        else:
            string += "F"

        if roleMeter.mayor == True:
            string += "T"
        else:
            string += "F"
        
        # if roleMeter.farmer == True:
        #     string += "T"
        # else:
        #     string += "F"

        # if roleMeter.doctor == True:
        #     string += "T"
        # else:
        #     string += "F"

        # if roleMeter.criminal == True:
        #     string += "T"
        # else:
        #     string += "F"
        if not is_evaluating :
            print("State: " + stateWord + " | Action: " + actionWord + " | Time: " + str(time) + " | Hp: " + str(hp) + " | Capacity: " + str(capacity) + " | Role: " + roleWord + " | Role Meter: " + string +  " | Score: " + str(total_score)) 

    print("REWARD: " + str(total_reward) + " | SCORE: " + str(total_score))

    if not is_evaluating:
        print("plotting...")
        rewardData.reverse()
        scoreData.reverse()

        x = timeData
        y = rewardData
        s = scoreData

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)

        ax.set_xlabel('time')
        ax.set_ylabel('reward')
        ax.scatter(x, y, label = 'reward', alpha = 0.5)
        ax.plot(x, y, label = 'reward', alpha = 0.5)
        #ax.plot(x, p(x), color= 'r' , linestyle = 'dashed', label = 'reward fit')
        ax.legend(loc='upper left')

        fig = plt.figure(figsize = (10, 5))
        ax1 = fig.add_subplot(1, 1, 1)

        ax1.set_xlabel('time')
        ax1.set_ylabel('score')
        ax1.scatter(x, s, label = 'score', alpha = 0.5, c = 'orange')
        ax1.plot(x, s, label = 'reward', alpha = 0.5, c = 'orange')
        #ax1.plot(x, ps(x), color= 'r', linestyle = 'dashed', label = 'score fit')
        ax1.legend(loc='upper left')
        plt.show()

    return total_reward, total_score