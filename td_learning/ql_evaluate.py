from audioop import avg
import copy
from enum import IntEnum
import numpy as np
from td_learning.ql_episode import episode
from td_learning.ql_runs import runs
import os
import matplotlib.pyplot as plt


def evaluate(env, time, hp, capacity, agent, n_runs=500, is_optimizing=False):
    #Train it for a certain # of episodes
    total_rewards = np.zeros(n_runs, dtype=float)
    total_scores = np.zeros(n_runs, dtype=float)

    print("Running RL (evaluating)...")
    for i in range(n_runs):
        env.reset(time, hp, capacity)
        reward, score = runs(env, time, hp, capacity, agent, True)
        total_rewards[i] = reward
        total_scores[i] = score

    sum = 0
    for i in total_rewards:
        sum += i
    avgReward = sum/n_runs

    sum = 0
    for i in total_scores:
        sum += i
    avgScore = sum/n_runs

    if not is_optimizing:
        print("AVERAGE REWARD: " + str(avgReward) + " | AVERAGE SCORE: " + str(avgScore))
        print("plotting...")
        
        x = list(range(0, n_runs))
        y = total_rewards
        s = total_scores

        z = np.polyfit(x, y, 1)
        zs = np.polyfit(x, s, 1)

        p = np.poly1d(z)
        ps = np.poly1d(zs)

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)

        ax.set_xlabel('runs')
        ax.set_ylabel('reward')
        ax.scatter(x, y, label = 'reward', alpha = 0.5)
        ax.axhline(y=avgReward, color='r', linestyle='dashed', label = 'Average reward')
        ax.legend(loc='upper left')

        fig = plt.figure(figsize = (10, 5))
        ax1 = fig.add_subplot(1, 1, 1)

        ax1.set_xlabel('runs')
        ax1.set_ylabel('score')
        ax1.scatter(x, s, label = 'score', alpha = 0.5, c = 'orange')
        ax1.axhline(y=avgScore, color='r', linestyle='dashed', label = 'Average score')
        ax1.legend(loc='upper left')
        plt.show()
        
    return avgReward, avgScore, total_rewards, total_scores