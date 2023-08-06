import copy
from enum import IntEnum
import numpy as np
from td_learning.ql_episode import episode
import os
import matplotlib.pyplot as plt


def train(env, time, hp, capacity, agent, n_episodes=500, is_optimizing=False):
    """
    Run multiple episodes with given environment and agent and return list of 
    total rewards for each episode. Agent's Q value persists through episodes.
    """

    #Train it for a certain # of episodes, and creates a new q_table
    total_rewards = np.zeros(n_episodes, dtype=float)
    total_scores = np.zeros(n_episodes, dtype=float)
    print("Running RL... (Training)")
    for i in range(n_episodes):
        env.reset(time, hp, capacity)
        reward, score = episode(env, time, hp, capacity, agent)
        total_rewards[i] = reward
        total_scores[i] = score
    
    #fig = plt.figure(figsize=(5, 5))
    #scat = fig.add_subplot(1, 1, 1)
    #scat.scatter(x, y, color = 'r')
    #scat.set_xlabel('episode')
    #scat.set_ylabel('reward/score')
    #scat.imshow()
        
    # env.reset(time)
    # done = False
    # total_reward = 0
    # state = agent.get_state_role()

    # while not done: #play thru the game
    #     action = agent.get_action(state, time) #get the action (dependent on epsilon, using epsilon-greedy algorithm)
    #     stateWord = ""
    #     if state == 0:
    #         stateWord = "zombie"
    #     elif state == 1:
    #         stateWord = "healthy"
    #     elif state == 2:
    #         stateWord = "injured"
    #     else:
    #         stateWord = "corpse"
        
    #     actionWord = ""
    #     if action == 0:
    #         actionWord = "save"
    #     elif action == 1:
    #         actionWord = "squish"
    #     elif action == 2:
    #         actionWord = "skip"
    #     elif action == 3:
    #         actionWord = "scram"

    #     print("State: " + stateWord + " | Action: " + actionWord + " | Time: " + str(time))
    #     next_state, next_time, next_hp, reward, done = env.step(action, state) #step the environment using the action
    #     state = next_state #update state
    #     time = next_time
    #     hp = next_hp
    #     total_reward += reward
    
    print("Writing to data file...")
    code_dir = os.path.dirname(__file__)
    file_path = os.path.join(code_dir, "q_table.txt")
    f = open(file_path, "w")
    for s in range(len(agent.q_table)):
        for t in range(len(agent.q_table[s])):
            for h in range(len(agent.q_table[s][t])):
                for c in range(len(agent.q_table[s][t][h])):
                    for r in range(len(agent.q_table[s][t][h][c])):
                        for rm in range(len(agent.q_table[s][t][h][c][r])):
                            for a in range(len(agent.q_table[s][t][h][c][r][rm])):
                                #print(agent.q_table[s][t][h][c][r][rm][a])
                                f.write(str(agent.q_table[s][t][h][c][r][rm][a]) + " ")
                            f.write("\n")
    f.close()

    if not is_optimizing: #only display plots when NOT optimizing to avoid plot clutter
        code_dir = os.path.dirname(__file__)
        file_path = os.path.join(code_dir, "total_reward.txt")
        f = open(file_path, "w")
        for r in range(len(total_rewards)):
            f.write(str(total_rewards[r]) + " ")
        f.write("\n")
        f.close()

        print("plotting...")
        
        x = list(range(0, n_episodes))
        y = total_rewards
        s = total_scores

        z = np.polyfit(x, y, 5)
        zs = np.polyfit(x, s, 5)

        p = np.poly1d(z)
        ps = np.poly1d(zs)

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)

        ax.set_xlabel('runs')
        ax.set_ylabel('reward')
        ax.scatter(x, y, label = 'reward', alpha = 0.1)
        ax.plot(x, p(x), color= 'r' , linestyle = 'dashed', label = 'reward fit')
        ax.legend(loc='upper left')

        fig = plt.figure(figsize = (10, 5))
        ax1 = fig.add_subplot(1, 1, 1)

        ax1.set_xlabel('runs')
        ax1.set_ylabel('score')
        ax1.scatter(x, s, label = 'score', alpha = 0.1, c = 'orange')
        ax1.plot(x, ps(x), color= 'r', linestyle = 'dashed', label = 'score fit')
        ax1.legend(loc='upper left')
        plt.show()
    
    
    

    return total_rewards