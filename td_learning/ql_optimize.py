from audioop import avg
import copy
from enum import IntEnum
import numpy as np
from td_learning.ql_enviornment import QLEnvironment
from td_learning.ql_agent import QLAgent
from td_learning.ql_train import train
from td_learning.ql_evaluate import evaluate
import os
import matplotlib.pyplot as plt


def optimize(epsilon_step=0.05, epsilon_start = 0.05, epsilon_end = 0.5):
    curr_epsilon = epsilon_start
    avgRewards = []
    avgScores = []
    epsilons = []
    while curr_epsilon <= epsilon_end:
        #train it with curr_epsilon
        print("Epsilon: " + str(curr_epsilon))
        time = 720
        hp = 10
        capacity = 10
        env = QLEnvironment(time, hp, capacity)
        agent = QLAgent(env.state_space, env.time_space, env.hp_space, env.capacity_space, env.role_space, env.roleMeter_space, env.action_space, curr_epsilon, 0.1, 1, True) 
        train(env, time, hp, capacity, agent, 50000, True)
        
        #evaluate it
        time = 720
        hp = 10
        capacity = 10
        env1 = QLEnvironment(time, hp, capacity)
        agent1 = QLAgent(env.state_space, env.time_space, env.hp_space, env.capacity_space, env.role_space, env.roleMeter_space, env.action_space, curr_epsilon, 0.1, 1, False) 
        avgReward, avgScore = evaluate(env1, time, hp, capacity, agent1, 500, True)

        avgRewards.append(avgReward)
        avgScores.append(avgScore)
        epsilons.append(curr_epsilon)

        curr_epsilon += epsilon_step

    print("plotting...")

    x = epsilons
    r = avgRewards
    s = avgScores

    z = np.polyfit(x, r, 5)
    zs = np.polyfit(x, s, 5)

    p = np.poly1d(z)
    ps = np.poly1d(zs)

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlabel('epsilon')
    ax.set_ylabel('reward')
    ax.plot(x, r, label = 'reward', alpha = 0.5)
    ax.plot(x, p(x), color= 'r' , linestyle = 'dashed', label = 'reward fit')
    ax.scatter(x, r, label = 'reward', alpha = 0.5)
    ax.legend(loc='upper left')

    fig = plt.figure(figsize = (10, 5))
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.set_xlabel('epsilon')
    ax1.set_ylabel('score')
    ax1.plot(x, ps(x), color= 'r' , linestyle = 'dashed', label = 'score fit')
    ax1.plot(x, s, label = 'score', alpha = 0.5, c = 'orange')
    ax1.scatter(x, s, label = 'score', alpha = 0.5, c = 'orange')
    ax1.legend(loc='upper left')

    plt.show()
    
    return 